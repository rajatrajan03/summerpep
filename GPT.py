from itertools import chain
import warnings
# import math
# import wandb
import os
import torch

warnings.filterwarnings("ignore")

# from hf
from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import DataCollatorForLanguageModeling
from transformers import GPT2Config, GPT2LMHeadModel0
from transformers import TrainingArguments, Trainer

# Create folders
os.makedirs("bookcorpus", exist_ok=True)
os.makedirs("gpt-2-warm-up", exist_ok=True)

# loading raw data
dataset = load_dataset("wikitext", "wikitext-2-raw-v1")

# make splits
dataset = dataset["train"].select(range(500))
dataset = dataset.train_test_split(test_size=50)

# load the gpt-2 tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

# tokenize
def tokenize_function(example):
    return tokenizer(text=example["text"])

tokenized_ds = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns="text"
)

# save to disk if required
# tokenized_ds.save_to_disk("bookcorpus/tokenized_ds")

# Make samples to a size of 1024
def concat(examples):
    examples["input_ids"] = [
        list(chain.from_iterable(examples["input_ids"]))
    ]
    examples["attention_mask"] = [
        list(chain.from_iterable(examples["attention_mask"]))
    ]
    return examples

# concatenate
# concatenate
concated_ds = tokenized_ds.map(
    concat,
    batched=True,
    batch_size=500
)

# chunking
def chunk(examples):

    chunk_size = 32

    input_ids = examples["input_ids"][0]
    attention_mask = examples["attention_mask"][0]

    input_ids_truncated = []
    attention_mask_truncated = []

    for i in range(0, len(input_ids), chunk_size):

        temp = input_ids[i:i + chunk_size]

        if len(temp) == chunk_size:

            input_ids_truncated.append(temp)

            attention_mask_truncated.append(
                attention_mask[i:i + chunk_size]
            )

    examples["input_ids"] = input_ids_truncated
    examples["attention_mask"] = attention_mask_truncated

    return examples


chunked_ds = concated_ds.map(
    chunk,
    batched=True,
    batch_size=2,
)

# chunked_ds.save_to_disk("bookcorpus/chunked_ds")

# data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer,
    mlm=False
)

# load model
configuration = GPT2Config(
    vocab_size=tokenizer.vocab_size,

    n_positions=32,
    n_ctx=32,

    n_embd=32,

    n_layer=1,

    n_head=1,

    bos_token_id=tokenizer.bos_token_id,
    eos_token_id=tokenizer.eos_token_id,
)

model = GPT2LMHeadModel(configuration)

total_params = sum(p.numel() for p in model.parameters())

print(f"Parameters: {total_params:,}")

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(device)

model.to(device)

if torch.cuda.is_available():
    torch.cuda.empty_cache()
    
# training arguments
training_args = TrainingArguments(
    output_dir="gpt-2-warm-up/standard-gpt",
    eval_strategy="steps",
    eval_steps=20,
    num_train_epochs=1,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    learning_rate=2.5e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    adam_beta1=0.9,
    adam_beta2=0.999,
    weight_decay=0.01,
    logging_strategy="steps",
    logging_steps=5,
    save_steps=100,
    save_total_limit=10,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    tokenizer=tokenizer,
    train_dataset=chunked_ds["train"],
    eval_dataset=chunked_ds["test"],
    data_collator=data_collator,
)

trainer.train()

trainer.save_model("gpt-2-warm-up/final")

# load trained model
model = GPT2LMHeadModel.from_pretrained(
    "gpt-2-warm-up/final"
).to(device)

prompt = "I was telling her that"

inputs = tokenizer(
    prompt,
    return_tensors="pt"
).input_ids.to(device)

outputs = model.generate(
    inputs,
    max_new_tokens=20,
    do_sample=True,
    top_k=10,
    top_p=0.95
)

print(tokenizer.batch_decode(outputs, skip_special_tokens=True)[0])