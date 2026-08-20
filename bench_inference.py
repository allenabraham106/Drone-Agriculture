import os
import time

import torch
import segmentation_models_pytorch as smp


def benchmark(model, device, batch_size, iters=20, warmup=5):
    x = torch.randn(batch_size, 3, 512, 512, device=device)
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        for _ in range(warmup):
            model(x)
        if device.type == "mps":
            torch.mps.synchronize()
        t0 = time.time()
        for _ in range(iters):
            model(x)
        if device.type == "mps":
            torch.mps.synchronize()
        t1 = time.time()
    total = t1 - t0
    ms_per_batch = total / iters * 1000
    ms_per_image = ms_per_batch / batch_size
    fps = 1000 / ms_per_image
    return ms_per_batch, ms_per_image, fps


def main():
    model = smp.Unet(encoder_name="resnet34", in_channels=3, classes=3)
    model.load_state_dict(torch.load("crop_model.pt", map_location="cpu"))
    model.eval()

    n_params = sum(p.numel() for p in model.parameters())
    model_bytes = os.path.getsize("crop_model.pt")
    print(f"Parameters: {n_params:,} ({n_params/1e6:.2f}M)")
    print(f"Checkpoint size: {model_bytes/1e6:.1f} MB")
    print()

    devices = [torch.device("cpu")]
    if torch.backends.mps.is_available():
        devices.append(torch.device("mps"))

    for device in devices:
        for batch_size in (1, 4):
            ms_batch, ms_img, fps = benchmark(model, device, batch_size)
            print(
                f"{device.type:>4} | batch={batch_size} | "
                f"{ms_batch:7.2f} ms/batch | {ms_img:7.2f} ms/image | {fps:6.1f} FPS"
            )


if __name__ == "__main__":
    main()
