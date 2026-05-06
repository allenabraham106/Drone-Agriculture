import torch 
import segmentation_models_pytorch as smp
import cv2
import numpy as np

def load_from_model(image_path, rows = 40, cols = 40):
    # load model
    model = smp.Unet(encoder_name="resnet34", in_channels=3, classes=3)
    model.load_state_dict(torch.load("crop_model.pt", map_location="cpu"))
    model.eval()

    # load a new image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (512, 512))

    # convert to tensor
    tensor = torch.tensor(image).permute(2, 0, 1).float() / 255.0
    tensor = tensor.unsqueeze(0)  # add batch dimension

    with torch.no_grad():
        output = model(tensor)
        predicted = output.argmax(dim = 1).squeeze().numpy()

    class_to_yield = {
        0 : "high",
        1 : "medium",
        2 : "low"
    }

    cell_h = 512 // rows
    cell_w = 512 // cols

    yield_zones ={

    }

    for row in range(rows):
        for col in range(cols):
            cell = predicted[row*cell_h: (row + 1)*cell_h, col*cell_w: (col + 1)*cell_w]
            values, counts = np.unique(cell, return_counts=True)
            dominant = values[np.argmax(counts)]
            yield_zones[(row, col)] = class_to_yield[dominant]
    
    return yield_zones
