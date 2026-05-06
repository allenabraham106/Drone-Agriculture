import torch
import segmentation_models_pytorch as smp
import cv2
import numpy as np

# load model
model = smp.Unet(encoder_name="resnet34", in_channels=3, classes=3)
model.load_state_dict(torch.load("crop_model.pt", map_location="cpu"))
model.eval()

# load a new image
image = cv2.imread("Feild.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (512, 512))

# convert to tensor
tensor = torch.tensor(image).permute(2, 0, 1).float() / 255.0
tensor = tensor.unsqueeze(0)  # add batch dimension

# predict
with torch.no_grad():
    output = model(tensor)
    predicted = output.argmax(dim=1).squeeze().numpy()

print(predicted.shape)
print("Unique classes predicted:", np.unique(predicted))
