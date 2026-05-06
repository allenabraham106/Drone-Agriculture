# 🚁 Ag-Drone Agricultural Path Planner

> A full ML perception pipeline meets precision agriculture, training a neural network on real CVPR research data to generate optimal drone harvest routes using A* pathfinding.

![Demo Screenshot](ScreenShot.png)

| Real Aerial Field Image | ML Model Output |
|------------------------|-----------------|
| ![Field](Feild.jpg) | ![ML Output](ML_Train.png) |

## Overview

Ag-Drone is a personal project and my first step into perception engineering and autonomous systems. It trains a UNet segmentation model on real labeled aerial crop imagery from the Agriculture Vision CVPR research dataset, classifies field zones by yield health, and uses a custom weighted A* pathfinding algorithm to deliver optimized harvest routes.

The project is highly adaptable. The same pipeline could be applied to wildfire suppression routing, search and rescue, or any scenario where terrain quality affects path priority.

## Inspiration

I have always been fascinated by Agriculture Technology. Companies like **MOSS Robotics** and **Upside Robotics** are building sensors and robots that give farmers real, actionable data about their fields. I wanted to take that idea one step further, not just display farm data, but use it to compute an optimal harvest route.

That question became this project: *"If a drone already knows which zones are healthy, how should it plan its route?"*

## How It Works

The simulation runs in three layers.

**1. ML Perception Pipeline (perception_model.py)**

A UNet segmentation model trained on the Agriculture Vision CVPR dataset predicts yield zones directly from any aerial RGB image. No mask files required — the model has learned what healthy and stressed crops look like from 2000 real labeled farm images.

The model outputs a pixel level classification for every cell:

🟢 High Yield — healthy crops with no detected anomaly

🟠 Medium Yield — double plant or mild stress detected

🟡 Low Yield — weed cluster, nutrient deficiency, planter skip, or storm damage detected

For reference, the dataset pipeline (perception_dataset.py) is also included for reading directly from Agriculture Vision mask files, and the RGB excess green index pipeline (perception.py) works on any unlabeled aerial image without the dataset.

**2. Pathfinding (astar.py)**

A* computes the optimal route from start to goal using the yield zone map produced by the perception pipeline. Unlike standard A*, this implementation uses yield weighted traversal costs:

| Zone | Cost |
|------|------|
| High Yield | 0.5 |
| Medium Yield | 1.0 |
| Low Yield | 2.0 |

Lower cost zones are naturally preferred, routing the drone through healthier crops and away from anomaly zones without any explicit instruction to do so.

**3. Drone Animation (drone.py)**

The drone animates step by step along the computed path, leaving a trail and accumulating a live yield score as it surveys each zone.

## Algorithm Deep Dive

A* works by maintaining a priority queue of cells to explore, always picking the cell with the lowest f score next:

```
f(n) = g(n) + h(n)

g = actual cost travelled from start
h = estimated cost to goal (Manhattan distance)
```

The key innovation is the custom cost function. Instead of treating every cell equally, each step's cost depends on the yield level predicted by the ML model. This means A* naturally routes through high yield zones and away from weed clusters or nutrient deficient areas.

## Model Training

The model is not included in this repo due to file size. Train it yourself:

**1. Download the Agriculture Vision 2017 dataset:**

```bash
aws s3 cp s3://intelinair-data-releases/agriculture-vision/cvpr_paper_2020/Dataset/data2017_miniscale.tar.gz . --no-sign-request
tar -xzf data2017_miniscale.tar.gz
```

**2. Train the model:**

```bash
python train.py
```

This trains a UNet with ResNet34 encoder on 2000 labeled aerial farm images using weighted CrossEntropy loss to handle class imbalance between healthy and anomaly zones. Training takes roughly 3 to 8 hours on Apple M4 GPU. The model is saved as `crop_model.pt`.

## Features

🧠 **Trained ML perception** UNet segmentation model predicts yield zones on any aerial image

🗺️ **Real dataset pipeline** reads expert labeled Agriculture Vision CVPR imagery directly

🤖 **Yield weighted A* pathfinding** naturally avoids weed clusters and anomaly zones

🚁 **Drone animation** step by step path visualization with live trail

📊 **Live dashboard** path length, current zone, yield score, yield percentage, estimated harvest value, and route rating

🌾 **Route rating** Excellent, Good, or Suboptimal based on yield efficiency

🚧 **Obstacle placement** simulate trees, buildings, or no fly zones

🔄 **Image cycling** press N and P to cycle through dataset images live

## How To Run

**Requirements:**

```bash
pip install pygame opencv-python numpy torch segmentation-models-pytorch
```

**Train the model first** using the instructions above, then:

```bash
python main.py
```

**Controls:**

| Key | Action |
|-----|--------|
| Left Click | Place start |
| G | Place goal at cursor |
| Right Click | Place obstacle |
| Space | Run A* and animate drone |
| N | Next dataset image |
| P | Previous dataset image |
| R | Generate procedural farm layout |

## Project Structure

```
ag-drone/
    main.py                  Pygame simulation, rendering, and event handling
    astar.py                 A* pathfinding algorithm with yield cost weights
    train.py                 UNet model training on Agriculture Vision dataset
    perception_model.py      ML model inference pipeline for any aerial image
    perception_dataset.py    Direct Agriculture Vision mask file pipeline
    perception.py            RGB excess green index pipeline for unlabeled imagery
    farm.py                  Procedural farm generation for testing
    drone.py                 Drone class, animation, scoring, and path tracking
    inference.py             Quick model inference test script
    drone.png                Drone sprite
    Feild.jpg                Sample aerial crop image
    README.md
```

## Stats and Metrics

**Path Length** is the total number of cells in the computed route

**Current Zone** shows the yield level of the drone's current cell

**Yield Score** is the accumulated score based on zones visited where High equals 3, Medium equals 2, and Low equals 1

**Yield %** compares actual yield score against the maximum possible score along the route

**Est. Harvest Value** converts the yield score into an estimated dollar value

**Route Rating** labels the run as Excellent at 80% and above, Good between 60 and 80%, and Suboptimal below 60%

## Future Work

ROS integration to publish computed paths as ROS topics for deployment on real autonomous drone hardware

3D terrain mapping to visualize elevation and crop height data

Multi drone coordination for covering different zones simultaneously

Fine tune on full Agriculture Vision dataset with all 8345 images for improved model accuracy

## Built With

Python, Pygame, OpenCV, NumPy, PyTorch, segmentation-models-pytorch, and the A* Search Algorithm

Dataset: [Agriculture Vision CVPR Dataset](https://www.agriculture-vision.com/)

*Inspired by [MOSS Robotics](https://www.moss.ag/) and [Upside Robotics](https://www.upsiderobotics.com/), companies building the future of precision agriculture.*