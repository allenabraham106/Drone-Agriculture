# 🚁 Ag-Drone Agricultural Path Planner

> A* pathfinding meets precision agriculture, optimizing drone harvest routes through procedurally generated crop fields.

![Demo Screenshot](screenshot.png)

## Overview

Ag-Drone is a 2 month personal project and my first step into path planning and autonomous systems. It uses a custom weighted A* algorithm to deliver optimized harvest routes for farmers based on crop yield zones.

The project is highly adaptable. The same algorithm could be applied to wildfire suppression routing, search and rescue, or any scenario where terrain quality affects path priority.

## Inspiration

I have always been fascinated by Agriculture Technology. Companies like **MOSS Robotics** and **Upside Robotics** are building sensors and robots that give farmers real, actionable data about their fields. I wanted to take that idea one step further, not just display farm data, but use it to compute an optimal harvest route.

That question became this project: *"If a drone already knows which zones are healthy, how should it plan its route?"*

## How It Works

The simulation runs in three layers.

**1. Farm Generation (farm.py)**

A procedural generator creates a randomized yield heatmap on startup and whenever R is pressed. Random seed points are placed on the grid, and each cell is assigned a yield level based on its distance to the nearest seed, mimicking how crop health naturally clusters in real fields.

🟢 High Yield represents dense, healthy crops

🟠 Medium Yield represents moderate crop health

🟡 Low Yield represents sparse or unhealthy crops

**2. Pathfinding (astar.py)**

A* computes the optimal route from start to goal. Unlike standard A*, this implementation uses yield weighted traversal costs:

| Zone | Cost |
|------|------|
| High Yield | 0.5 |
| Medium Yield | 1.0 |
| Low Yield | 2.0 |

Lower cost zones are naturally preferred, routing the drone through healthier crops.

**3. Drone Animation (drone.py)**

The drone animates step by step along the computed path, leaving a trail and accumulating a live yield score as it surveys each zone.

## ⚠️ Disclaimer

This project was built with the assumption that yield data has already been collected. In a real deployment this data would come from LiDAR scans, multispectral imaging, or NDVI satellite data, the same sensors used by companies like MOSS. The generate_farm() function would simply be replaced by a real data parser. The A* pathfinding layer is completely sensor agnostic.

Integrating real sensor inputs is something I would love to explore with access to the right hardware.

## Algorithm Deep Dive

A* works by maintaining a priority queue of cells to explore, always picking the cell with the lowest f score next:

```
f(n) = g(n) + h(n)

g = actual cost travelled from start
h = estimated cost to goal (Manhattan distance)
```

The key innovation here is the custom cost function. Instead of treating every cell equally, each step's cost depends on the yield level of the cell being entered. This means A* naturally routes through high yield zones, not because it is told to avoid low yield, but because high yield cells are simply cheaper to traverse.

The came_from dictionary tracks the breadcrumb trail, allowing full path reconstruction once the goal is reached.

## Features

🗺️ **Procedural farm generation** randomized yield heatmap on every run

🧠 **Yield weighted A* pathfinding** algorithm naturally prioritizes high value crop zones

🚁 **Drone animation** step by step path visualization with live trail

📊 **Live dashboard** path length, current zone, yield score, yield percentage, estimated harvest value, and route rating

🌾 **Route rating** Excellent, Good, or Suboptimal based on yield efficiency

🚧 **Obstacle placement** simulate trees, buildings, or no fly zones

🔄 **Farm regeneration** press R for a new randomized layout

## How To Run

**Requirements:**
```bash
pip install pygame
```

**Controls:**

| Key | Action |
|-----|--------|
| Left Click | Place start |
| G | Place goal at cursor |
| Right Click | Place obstacle |
| Space | Run A* and animate drone |
| R | Generate new farm |

## Project Structure

```
ag-drone/
    main.py        Pygame simulation, rendering, and event handling
    astar.py       A* pathfinding algorithm with yield cost weights
    farm.py        Procedural farm generation
    drone.py       Drone class, animation, scoring, and path tracking
    drone.png      Drone sprite
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

Real sensor integration would replace procedural generation with NDVI or multispectral drone data

3D terrain mapping would visualize elevation and crop height data in three dimensions

Multi drone coordination would allow multiple drones to cover different zones simultaneously

Coverage pathfinding would optimize for visiting all high yield zones rather than just navigating from start to goal

OpenCV integration would process simulated aerial camera frames into yield zone maps

## Built With

Python, Pygame, and the A* Search Algorithm

*Inspired by [MOSS Robotics](https://www.moss.ag/) and [Upside Robotics](https://www.upsiderobotics.com/), companies building the future of precision agriculture.*