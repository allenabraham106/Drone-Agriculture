import cv2
import numpy as np
import os

def load_from_dataset(dataset_path, image_name, rows = 40, cols = 40):
    anomaly_to_yield = {
        "double_plant": "medium",
        "drydown": "low",
        "nutrient_deficiency": "low",
        "planter_skip": "low",
        "storm_damage": "low",
        "weed_cluster": "low",
        "water": "low",
        "waterway": "low",
    }
    yield_map = np.full((512, 512), "high", dtype = object)
    yield_zones = {

    }
    cell_h = 512 // rows
    cell_w = 512 // cols

    for anomaly in anomaly_to_yield:
        mask_name = image_name.replace(".jpg", ".png")
        mask_path = os.path.join(dataset_path, "field_labels", anomaly, mask_name)
        if os.path.exists(mask_path):
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE) # turns into grayscale
            yield_map[mask == 255] = anomaly_to_yield[anomaly] #checks if there is an anomaly at that pixel and associates to a level

    for row in range(rows):
        for col in range(cols):
            cell = yield_map[row*cell_h: (row + 1)*cell_h, col * cell_w: (col + 1)*cell_w] #looks at a chunk of the map and the pixels that belong to it
            value, counts = np.unique(cell, return_counts=True) # keep track of the different levels 
            yield_zones[(row, col)] = value[np.argmax(counts)] # whichever yield level appears most is what the zone is
    return yield_zones


if __name__ == "__main__":
    dataset_path = "data2017_miniscale"
    image_name = "16RQA6NB1_2362-523-2874-1035.jpg"
    zones = load_from_dataset(dataset_path, image_name)
    print(zones)
