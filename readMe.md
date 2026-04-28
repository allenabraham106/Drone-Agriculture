# 🚁 Ag-Drone Agricultural Path Planner

> A computer vision perception pipeline meets precision agriculture, processing real aerial drone imagery to generate optimal harvest routes using A* pathfinding.

![Demo Screenshot](Screenshot.png)

## Overview

Ag-Drone is a 2 month personal project and my first step into perception engineering and autonomous systems. It uses OpenCV to process real aerial crop imagery, extracts vegetation health data using excess green index analysis, and feeds that structured data into a custom weighted A* pathfinding algorithm to deliver optimized harvest routes.

The project is highly adaptable. The same pipeline could be applied to wildfire suppression routing, search and rescue, or any scenario where terrain quality affects path priority.

| Original Field Image | Perception Output |
|---------------------|-------------------|
| ![Field](Field.jpg) | ![Perception](Perception_Results.png) |


## Inspiration

I have always been fascinated by Agriculture Technology. Companies like **MOSS Robotics** and **Upside Robotics** are building sensors and robots that give farmers real, actionable data about their fields. I wanted to take that idea one step further, not just display farm data, but use it to compute an optimal harvest route.

That question became this project: *"If a drone already knows which zones are healthy, how should it plan its route?"*

## How It Works

The simulation runs in three layers.

**1. Perception Pipeline (perception.py)**

A computer vision pipeline processes a real aerial crop image using OpenCV. The image is resized to match the simulation grid, split into RGB channels, and analyzed cell by cell using the Excess Green Index, a real vegetation health metric used in precision agriculture:

```
Excess Green = Average Green Channel  Average Red Channel
```

Each grid cell is classified based on its vegetation health:

🟢 High Yield represents dense, healthy crops with strong green dominance

🟠 Medium Yield represents moderate crop health with balanced channels

🟡 Low Yield represents stressed or sparse crops with reduced green response

This is the same core principle behind NDVI analysis used by real agri-tech companies, applied to standard RGB imagery.

**2. Pathfinding (astar.py)**

A* computes the optimal route from start to goal using the yield zone map produced by the perception pipeline. Unlike standard A*, this implementation uses yield weighted traversal costs:

| Zone | Cost |
|------|------|
| High Yield | 0.5 |
| Medium Yield | 1.0 |
| Low Yield | 2.0 |

Lower cost zones are naturally preferred, routing the drone through healthier crops without any explicit instruction to do so.

**3. Drone Animation (drone.py)**

The drone animates step by step along the computed path, leaving a trail and accumulating a live yield score as it surveys each zone.

## Algorithm Deep Dive

A* works by maintaining a priority queue of cells to explore, always picking the cell with the lowest f score next:

```
f(n) = g(n) + h(n)

g = actual cost travelled from start
h = estimated cost to goal (Manhattan distance)
```

The key innovation here is the custom cost function. Instead of treating every cell equally, each step's cost depends on the yield level detected by the perception pipeline. This means A* naturally routes through high yield zones, not because it is told to avoid low yield, but because high yield cells are simply cheaper to traverse.

The came_from dictionary tracks the breadcrumb trail, allowing full path reconstruction once the goal is reached.

## Features

🗺️ **Real aerial image processing** OpenCV pipeline extracts vegetation health from actual drone imagery

🧠 **Yield weighted A* pathfinding** algorithm naturally prioritizes high value crop zones

🚁 **Drone animation** step by step path visualization with live trail

📊 **Live dashboard** path length, current zone, yield score, yield percentage, estimated harvest value, and route rating

🌾 **Route rating** Excellent, Good, or Suboptimal based on yield efficiency

🚧 **Obstacle placement** simulate trees, buildings, or no fly zones

🔄 **Farm regeneration** press R to generate a new procedural farm layout for testing

## How To Run

**Requirements:**
```bash
pip install pygame opencv-python
```

**Add your field image:**

Place an aerial crop image named `Field.jpg` in the project root. The perception pipeline will automatically process it into yield zones on startup.

**Controls:**

| Key | Action |
|-----|--------|
| Left Click | Place start |
| G | Place goal at cursor |
| Right Click | Place obstacle |
| Space | Run A* and animate drone |
| R | Generate procedural farm layout |

## Project Structure

```
ag-drone/
    main.py        Pygame simulation, rendering, and event handling
    astar.py       A* pathfinding algorithm with yield cost weights
    perception.py  OpenCV pipeline, image loading, excess green analysis, yield zone classification
    farm.py        Procedural farm generation for testing
    drone.py       Drone class, animation, scoring, and path tracking
    drone.png      Drone sprite
    field.jpg      Aerial crop image input
    README.md
```

## Stats and Metrics

The dashboard tracks the following live metrics:

**Path Length** is the total number of cells in the computed route

**Current Zone** shows the yield level of the drone's current cell

**Yield Score** is the accumulated score based on zones visited where High equals 3, Medium equals 2, and Low equals 1

**Yield %** compares actual yield score against the maximum possible score along the route

**Est. Harvest Value** converts the yield score into an estimated dollar value

**Route Rating** labels the run as Excellent at 80% and above, Good between 60 and 80%, and Suboptimal below 60%

## Future Work

NDVI integration would replace the RGB excess green index with true multispectral NDVI analysis using near infrared channel data, the same sensor modality used by MOSS Robotics

3D terrain mapping would visualize elevation and crop height data in three dimensions

Multi drone coordination would allow multiple drones to cover different zones simultaneously

Coverage pathfinding would optimize for visiting all high yield zones rather than just navigating from start to goal

ROS integration would publish computed paths as ROS topics, enabling deployment on real autonomous drone hardware

## Built With

Python, Pygame, OpenCV, and the A* Search Algorithm

*Inspired by [MOSS Robotics](https://www.moss.ag/) and [Upside Robotics](https://www.upsiderobotics.com/), companies building the future of precision agriculture.*