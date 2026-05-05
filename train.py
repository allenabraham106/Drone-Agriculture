import torch 
import segmentation_models_pytorch as smp
import cv2
import numpy as np
import os

# unet is industry standard for segmentation
model = smp.Unet(
    encoder_name = "resnet34", # pretrained model that is able to see shapes and edges
    in_channels=3, # 3 chanels - Red Green Blue
    classes=3 # 3 classes - High, Medium, Low yields
)

class CropDataset:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.images = os.listdir(os.path.join(dataset_path, "field_images/rgb"))
        self.images.sort()
    def __len__(self):
        return len(self.images)
    def __getitem__(self, index):
        image_name = self.image[index]
        image_path = os.path.join(self.dataset_path, "field_images/rgb", image_name)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


