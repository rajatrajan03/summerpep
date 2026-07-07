SUMMERPEP
A playground of algorithms, ML experiments, and a LeetCode solving extension scaffold

PythonJavaScriptHTML5CSS3StarsForksBranch
🚀 What is this?
Summerpep is a multi-domain playground that folds together learning-oriented code samples across data structures, object‑oriented programming, and machine learning, plus a Chrome extension scaffold intended for LeetCode assistance. The repository hosts self-contained demonstrations and experiments in:

Fundamentals: DSA basics, OOP patterns, and common design principles.
ML / CV experiments: ANN, KNN, Transformer models (with multi-head attention), Vision Transformer, YOLOv1 preprocessing/output scaffolding, and a CIFAR-10 data asset.
Web extension scaffolding: A Solverr extension skeleton with manifest, content scripts, messaging, and UI elements.
The codebase is a mix of Python (ML demos) and JavaScript/HTML/CSS (extension UI and chrome-extension scaffolding), with supporting assets and documentation in Solverr and ML folders.

Key folders and what they contain (high level):

ANN.py, KNN.py, DSA/basics.py, OOPsbasics.py, pattern.py — foundational algorithm/demos and object-oriented examples.
Transformer.py, VisonTransformer/Vision_transformer.py — ML model scaffolding using PyTorch.
VisonTransformer/data/cifar-10-python.tar.gz — CIFAR-10 data asset.
YoloV1/YoloV1.py — You Only Look Once v1 related demo and preprocessing scaffold.
Solverr/ — Chrome extension scaffolding: architecture doc, README, manifest, background/content scripts, messaging, and popup UI.
Solverr/utils/* — helper utilities, constants, defaults, storage abstractions.
Solverr/api/ai.js, Solverr/content/* — extension integration points.
Solverr/ARCHITECTURE.md, Solverr/README.md, Solverr/TODO.md — docs for extension architecture and roadmap.
Transformer.py, VisonTransformer directory — ML model implementation notes and data.
Recent commits (highlights)

Implemented ANN and leetcode-solving extension scaffolding (d26afee) 🧠🧩
Added KNN basics (11d0797) 🧭
Initial YOLOv1 model/data preprocessing & output generation (4e36670) 🚀🛈
Transformer model with multi-head attention and feed-forward (beca967) 🔎🧠
OOP examples: abstraction, encapsulation, inheritance (5cb5d92 / 1e74ebc / 5162f88) 🧱✨
Cleanup and readability improvements in pattern.py and related examples (ed79f7b, 9c91cbb) 🧽
Tech stack

Python (core ML demos and scripts: ANN, Transformer, YOLO, Vision Transformer, DSA/OOP samples)
PyTorch (as noted in Transformer and Vision Transformer implementations)
JavaScript, HTML, CSS (Solverr Chrome extension scaffold and UI)
Data assets (CIFAR-10 tarball included for quick experimentation)
JSON / manifest.json (extension metadata)
✨ Features
DSA & OOP Tutorials

Practical basics and patterns via files like DSA/basics.py and OOPsbasics.py
Abstraction, encapsulation, inheritance, and multilevel/inheritance examples
Pattern.py cleanup and demonstrations
ML / DL Experiments

ANN.py: Artificial Neural Network demo and intuition
KNN.py: K-Nearest Neighbors basics
Transformer.py: Transformer with multi-head attention and feed-forward layers (PyTorch)
VisonTransformer/Vision_transformer.py: Vision Transformer scaffolding
YoloV1/YoloV1.py: YoloV1 model scaffolding with data preprocessing and output generation
CIFAR-10 data asset included for experiments
Chrome Extension Skeleton (Solverr)

Starter architecture for a LeetCode-solving extension
Architecture doc (ARCHITECTURE.md) and README under Solverr
Core pieces: manifest.json, background.js, content scripts (editor.js, extractor.js, messaging.js, parser.js), popup UI (popup.html, popup.js, popup.css)
Storage, utilities, and API scaffolding (utils/*, api/ai.js)
Data & Assets

CIFAR-10 dataset bundle included for immediate toy experiments
Directory structure designed to separate ML demos from extension scaffolding for clarity
🛠 Installation
Prerequisites (developer experience)

Python 3.x
PyTorch (for Transformer / Vision Transformer / YOLO demos)
Optional: pip for Python dependencies
A Chrome-compatible browser to load the Solverr extension (no build steps required)
Step-by-step

Clone the repository
git clone https://github.com/rajatrajan03/summerpep
cd summerpep
Python ML demos (ANN, KNN, Transformer, Vision Transformer, YOLO)
Ensure Python 3.x is installed
For PyTorch-enabled demos, install PyTorch (visit https://pytorch.org for the right command)
Basic invocation examples (each file is a self-contained script or module; run or import as needed):
python3 ANN.py
python3 KNN.py
python3 Transformer.py
python3 VisonTransformer/Vision_transformer.py
python3 YoloV1/YoloV1.py
python3 DSA/basics.py
python3 OOPsbasics.py
python3 pattern.py
Chrome extension: Solverr scaffold
Open Chrome -> chrome://extensions
Enable Developer mode
Click "Load unpacked" and select the Solverr directory
Explore the extension’s architecture and UI (popup, content scripts, messaging, and API hooks)
Data assets
If you want to explore CIFAR-10, extract VisonTransformer/data/cifar-10-python.tar.gz and feed it into the Vision Transformer flow as needed
Notes

There is no single install command for all components because the repo is a stitched-together collection of independent demos. Treat each folder/file as a standalone experiment or example.
If you want to install additional Python dependencies, you can create a local virtual environment and install packages as needed (e.g., PyTorch, numpy, pillow, torchvision, etc.).
🎮 How to use
DSA, OOP, and pattern demos

Each file is designed to be run as a standalone Python script. For example:
python3 DSA/basics.py to see data structure demonstrations
python3 OOPsbasics.py to view basic OOP examples
Inspect the code for usage examples, classes, and functions. They’re educational snippets meant for learning and experimentation.
Machine Learning demos

ANN.py, KNN.py, Transformer.py, Vision Transformer, and YOLO v1 scripts are self-contained demonstrations relying on PyTorch and standard ML libraries.
Example run sequence (adjusted to your environment and data):
python3 ANN.py
python3 KNN.py
python3 Transformer.py
python3 VisonTransformer/Vision_transformer.py
python3 YoloV1/YoloV1.py
Some scripts may require command-line arguments or dataset preparation steps; refer to the script headers or inline comments for specifics.
Solverr extension

The Solverr folder contains a Chrome extension scaffold (manifest.json, background.js, content scripts, popup UI, etc.).
Load the folder into Chrome as an unpacked extension and explore how the extension communicates via messaging.js, parser.js, and editor.js.
The included ARCHITECTURE.md and Solverr/README.md provide deeper context on how the extension is intended to function.
Data assets

CIFAR-10 tarball is included for quick experimentation with the Vision Transformer demo. You can extract it locally and wire it into the data pipeline as needed.
🤝 Contributing
Love the mix of algorithms, ML experiments, and extension scaffolds? We’d love contributors!

Contribution ideas

Add more DSA or OOP examples (in their respective Python files) with clear commentary.
Expand ML demos: add training loops, evaluation scripts, or small utilities around Transformer and Vision Transformer.
Improve the Solverr extension scaffold: add more features, robust messaging, error handling, or a tiny demo LeetCode workflow.
Update architecture docs in Solverr/ARCHITECTURE.md or Solverr/README.md with clearer diagrams.
Update or add datasets to the Vision Transformer flow (e.g., different toy datasets, data loaders).
How to contribute

Fork the repo and create a feature branch: git checkout -b feat/your-feature
Implement changes with clear, well-documented code
Run existing demos to ensure compatibility
Submit a PR against main with a descriptive summary of your changes
Code style and guidelines

Python: prefer readability (PEP8-ish guidance), docstrings, and clear function/class names
JavaScript/HTML/CSS: keep UI code clean; add comments where necessary
Documented changes: update README sections or add a short CONTRIBUTING note in Solverr/README.md as needed
Community and docs

Solverr/ARCHITECTURE.md and Solverr/README.md provide architectural context for the extension scaffold.
The repository’s recent commits show active expansion into ML models (ANN, Transformer, YOLO), OOP/DSA examples, and the extension scaffold.
If you’d like, I can tailor this README further to emphasize a particular component (e.g., focus more on the ML experiments or the Solverr extension) or generate a concise quick-start guide for beginners.

