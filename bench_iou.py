import time

import numpy as np
import torch
import segmentation_models_pytorch as smp
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
        ious.append(float("nan") if union == 0 else intersection / union)
    return ious


def main():
    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

    model = smp.Unet(encoder_name="resnet34", in_channels=3, classes=3)
    model.load_state_dict(torch.load("crop_model.pt", map_location="cpu"))
    model.to(device)
    model.eval()

    all_images = sorted(__import__("os").listdir("data2017_miniscale/field_images/rgb"))[:8345]
    split = int(0.8 * len(all_images))
    val_images = all_images[split:]

    val_dataset = CropDataset("data2017_miniscale")
    val_dataset.images = val_images
    # disable random augmentation for a clean eval pass, keep normalization/tensor conversion
    import albumentations as A
    from albumentations.pytorch import ToTensorV2
    val_dataset.transform = A.Compose([
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2(),
    ])

    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=0)

    print(f"Evaluating on {len(val_images)} validation images (device={device.type})")
    t0 = time.time()
    all_ious = []
    with torch.no_grad():
        for images, masks in val_loader:
            images = images.to(device)
            outputs = model(images)
            preds = outputs.argmax(dim=1).cpu()
            for pred, mask in zip(preds, masks):
                all_ious.append(calculate_iou(pred, mask))
    t1 = time.time()

    mean_ious = np.nanmean(all_ious, axis=0)
    print(f"IoU High Yield:   {mean_ious[0]:.3f}")
    print(f"IoU Medium Yield: {mean_ious[1]:.3f}")
    print(f"IoU Low Yield:    {mean_ious[2]:.3f}")
    print(f"Mean IoU:         {np.nanmean(mean_ious):.3f}")
    print(f"Eval wall time:   {t1 - t0:.1f}s for {len(val_images)} images "
          f"({(t1 - t0) / len(val_images) * 1000:.1f} ms/image incl. dataloading)")


if __name__ == "__main__":
    main()
