import torch
import segmentation_models_pytorch as smp
import numpy as np
import os
from torch.utils.data import DataLoader
from train import CropDataset


def calculate_iou(pred, target, num_classes=3):
    ious = []
    pred = pred.cpu().numpy()
    target = target.cpu().numpy()
    for cls in range(num_classes):
        pred_cls = pred == cls
        target_cls = target == cls
        intersection = (pred_cls & target_cls).sum()
        union = (pred_cls | target_cls).sum()
        if union == 0:
            ious.append(float("nan"))
        else:
            ious.append(intersection / union)
    return ious


model = smp.Unet(encoder_name="resnet34", in_channels=3, classes=3)
model.load_state_dict(torch.load("crop_model.pt", map_location="cpu"))
model.eval()

all_images = os.listdir("data2017_miniscale/field_images/rgb")
all_images.sort()
all_images = all_images[:8345]
split = int(0.8 * len(all_images))
val_images = all_images[split:]

val_dataset = CropDataset("data2017_miniscale")
val_dataset.images = val_images
val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)

all_ious = []
with torch.no_grad():
    for images, masks in val_loader:
        outputs = model(images)
        preds = outputs.argmax(dim=1)
        for pred, mask in zip(preds, masks):
            ious = calculate_iou(pred, mask)
            all_ious.append(ious)

mean_ious = np.nanmean(all_ious, axis=0)
print(f"IoU High Yield: {mean_ious[0]:.3f}")
print(f"IoU Medium Yield: {mean_ious[1]:.3f}")
print(f"IoU Low Yield: {mean_ious[2]:.3f}")
print(f"Mean IoU: {np.nanmean(mean_ious):.3f}")
