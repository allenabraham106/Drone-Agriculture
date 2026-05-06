import torch 
import segmentation_models_pytorch as smp
import cv2
import numpy as np
import os
from torch.utils.data import Dataloader

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
        image_name = self.images[index]
        image_path = os.path.join(self.dataset_path, "field_images/rgb", image_name)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        anomaly_to_yield = {
            "double_plant": 1,
            "drydown": 2,
            "nutrient_deficiency": 2,
            "planter_skip": 2,
            "storm_damage": 2,
            "weed_cluster": 2,
            "water": 2,
            "waterway": 2,
        }
    
        mask = np.zeros((512, 512), dtype = np.int64)
        for anomoly, class_id in anomaly_to_yield.items():
            mask_name = image_name.replace(".jpg", ".png")
            mask_path = os.path.join(self.dataset_path, "field_labels", anomoly, mask_name)
            if os.path.exists(mask_path):
                anomoly_mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
                mask[anomoly_mask == 255] = class_id  #creates a true or false grid, true if anomoly exists

        #reorders the grid and converst to a tensor
        image = torch.tensor(image).permute(2, 0, 1).float() / 255.0
        mask = torch.tensor(mask).long()

        return image, mask


dataset = CropDataset("data2017_miniscale")
dataloader = Dataloader(dataset, batch_size = 4, suffle = True)
loss_function = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.001) # this adds weights based on our loss function. 0.001 is a default but safe
