import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import  xml.etree.ElementTree as ET
import cv2
import shutil
import torch
import os
from torch.utils.data import TensorDataset, DataLoader

train_images="JPEGImages/"
train_maps="Annotations/"

classes=['aeroplane','bicycle','bird','boat','bottle','bus','car','cat','chair','cow','diningtable','dog','horse','motorbike','person','pottedplant','sheep','sofa','train','tvmonitor']

N_CLASSES=len(classes)
H,W=224,224
SPLIT_SIZE=int(H/32)
BATCH_SIZE=32

# This function preprocesses an XML file containing object detection annotations.
def preprocess_xml(filename):
    
    # Parse the XML file using ElementTree.
    tree = ET.parse(filename)
    root = tree.getroot()
    
    # Extract image size from the XML.
    size_tree = root.find('size')
    height = float(size_tree.find('height').text)
    width = float(size_tree.find('width').text)
    
    # Initialize list to store bounding boxes.
    bounding_boxes = []
    
    # Create a dictionary to map class names to indices.
    class_dict = {classes[i]: i for i in range(len(classes))}
    
    # Iterate through each object annotation in the XML.
    for object_tree in root.findall('object'):
        # Extract bounding box coordinates.
        for bounding_box in object_tree.iter('bndbox'):
            xmin = float(bounding_box.find('xmin').text)
            xmax = float(bounding_box.find('xmax').text)
            ymin = float(bounding_box.find('ymin').text)
            ymax = float(bounding_box.find('ymax').text)
            break
        
        # Extract class name of the object.
        class_name = object_tree.find('name').text
        
        # Calculate normalized bounding box coordinates and append to the list.
        bounding_box = [
            (xmin + xmax) / (2 * width),
            (ymin + ymax) / (2 * height),
            (xmax - xmin) / width,
            (ymax - ymin) / height,
            class_dict[class_name]
        ]
        bounding_boxes.append(bounding_box)
    
    # Convert the list of bounding boxes to a TensorFlow tensor and return.
    return torch.tensor(bounding_boxes)

def generate_output(bounding_boxes):
    # Initialize output label tensor
    output_label = np.zeros((SPLIT_SIZE, SPLIT_SIZE, N_CLASSES + 5))

    # Iterate through bounding boxes
    for b in range(len(bounding_boxes)):
        # Calculate grid positions
        grid_x = bounding_boxes[..., b, 0] * SPLIT_SIZE
        grid_y = bounding_boxes[..., b, 1] * SPLIT_SIZE
        
        # Convert to integer grid indices
        i = int(grid_x)
        j = int(grid_y)

        # Assign values to output label tensor
        output_label[i, j, 0:5] = [1., grid_x % 1, grid_y % 1, bounding_boxes[..., b, 2], bounding_boxes[..., b, 3]]
        output_label[i, j, 5 + int(bounding_boxes[..., b, 4])] = 1.

    # Convert output label tensor to TensorFlow tensor
    return torch.tensor(output_label)

im_paths=[]
xml_paths=[]

for i in os.listdir(train_maps)[:500]:
    im_paths.append(train_images+i[:-3]+'jpg')
    xml_paths.append(train_maps+i)
    
import torchvision.transforms as transforms
from PIL import Image

# Define transformations
transform = transforms.Compose([
    transforms.Resize((H, W)),
    transforms.ToTensor(),
])

images = []
for im_path in im_paths:
    # Open image using PIL
    img = Image.open(im_path).convert('RGB')
    
    # Apply transformations
    img_tensor = transform(img)
    
    images.append(img_tensor)

# Stack tensors
images = torch.stack(images)


boxes = []

for xml_path in xml_paths:
    
    boxes.append(generate_output(preprocess_xml(xml_path)))
    
boxes = torch.stack(boxes).float()

print("Images Shape:", images.shape)
print("Boxes Shape:", boxes.shape)
print("Dataset Loaded Successfully!")