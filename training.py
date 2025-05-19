import os
import sys

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
import yaml
from ultralytics import YOLO
from utils.utils import read_yaml


# Load training configuration from YAML
config = read_yaml('params.yaml')

# Dataset and model settings
data_path = config["dataset"]["path"]
train_data = config["dataset"]["train"]
val_data = config["dataset"]["val"]
nc = config["dataset"]["nc"]
names = config["dataset"]["names"]
MODEL_NAME = config['model']['type']

# Training parameters
EPOCHS = config['training']['epochs']
IMG_SIZE = config['training']['img_size']
BATCH_SIZE = config['training']['batch_size']
DEVICE = 'cpu' #config['training']['device']
WORKERS = config['training']['workers']
PROJECT = config['training']['project']
NAME = config['training']['name']

# Optional hyperparameters (if needed)
LR0 = config['hyperparameters'].get('lr0', 0.01)
LRF = config['hyperparameters'].get('lrf', 0.1)
MOMENTUM = config['hyperparameters'].get('momentum', 0.937)
WEIGHT_DECAY = config['hyperparameters'].get('weight_decay', 0.0005)

with open("data.yaml", "w") as f:
    yaml.dump({
        "path": data_path,
        "train": train_data,
        "val": val_data,
        "nc": nc,
        'names':names
    }, f)


# Initialize YOLO model
model = YOLO(MODEL_NAME)

# Train the model
model.train(
    data='data.yaml',
    epochs=EPOCHS,
    imgsz=IMG_SIZE,
    batch=BATCH_SIZE,
    device=DEVICE,
    workers=WORKERS,
    project=PROJECT,
    name=NAME,
    lr0=LR0,
    lrf=LRF,
    momentum=MOMENTUM,
    weight_decay=WEIGHT_DECAY
)

# Evaluate the model on validation set
metrics = model.val()
print("Validation Results:", metrics)
