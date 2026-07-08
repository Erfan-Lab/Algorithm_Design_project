# 🚚 Smart City Routing System

> A Python implementation of an intelligent routing engine that computes optimal delivery routes using graph algorithms and dynamic road conditions.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Algorithms](https://img.shields.io/badge/Algorithms-Dijkstra%20%7C%20Bellman--Ford-green)
![Graph](https://img.shields.io/badge/Data%20Structure-Adjacency%20List-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📖 Overview

This project was developed as part of a **Design and Analysis of Algorithms** course.

The system models a city as a **directed weighted graph**, where:

- 🛣️ Vertices represent intersections.
- 🚦 Edges represent roads.
- ⏱️ Each intersection has a delay time.
- 🚗 Traffic conditions affect travel cost.
- 🌧️ Weather conditions affect travel cost.

The program automatically chooses the most appropriate shortest-path algorithm depending on whether the graph contains negative edge weights.

---

## ✨ Features

- 📍 Build a graph from a text file
- ⚡ Dynamic edge cost calculation
- 🚀 Dijkstra's shortest path algorithm
- 🔄 Bellman-Ford shortest path algorithm
- ❗ Negative cycle detection
- 🗺️ Path reconstruction
- 📦 Multiple destination routing
- 🎯 Nearest Neighbor heuristic for delivery optimization

---

## 🧮 Edge Cost Formula

Each road cost is calculated as

```text
Cost(u, v) =
(distance × traffic_coefficient × weather_coefficient)
+ destination_delay
```

where

- **distance** = Road length
- **traffic_coefficient** = Current traffic condition
- **weather_coefficient** = Road/weather condition
- **destination_delay** = Delay at the destination intersection

---

## 📂 Input Format

The graph is loaded from a file named **`map.txt`**.

### Vertex

```text
V <VertexID> <Delay>
```

Example

```text
V A 3
V B 2
V C 5
```

### Edge

```text
E <Source> <Destination> <Distance> <Traffic> <Weather>
```

Example

```text
E A B 10 1.2 1.5
E B C 8 1.0 2.0
```

---

## 🏗️ Project Structure

```text
project/
│
├── main.py
├── map.txt
└── README.md
```

---

## 🧠 Algorithms Used

### 🚀 Dijkstra

Used when **all edge weights are non-negative**.

**Time Complexity**

```text
O((V + E) log V)
```

---

### 🔄 Bellman-Ford

Automatically selected whenever the graph contains **negative edge weights**.

Features:

- Finds shortest paths
- Detects negative cycles

**Time Complexity**

```text
O(VE)
```

---

### 📦 Nearest Neighbor Heuristic

Used for routing through multiple delivery destinations.

Steps:

1. Start from the source.
2. Visit the closest unvisited destination.
3. Repeat until every destination is visited.
4. Return to the starting point.

---

## 🔍 Main Functions

| Function | Description |
|----------|-------------|
| `build_graph()` | Loads the graph from `map.txt` |
| `shortest_path_dijkstra()` | Computes shortest paths using Dijkstra |
| `shortest_path_bellman_ford()` | Computes shortest paths using Bellman-Ford |
| `find_optimal_shortest_path()` | Automatically selects the appropriate algorithm |
| `multiple_destinations_shortest_path()` | Finds an efficient multi-stop delivery route |
| `build_path()` | Reconstructs the shortest path |

---

## 💡 Algorithm Selection

```text
Negative Edge?
        │
   ┌────┴────┐
   │         │
  No        Yes
   │         │
Dijkstra  Bellman-Ford
```

---

## 📊 Data Structures

- Dictionary
- Adjacency List
- Min Heap (`heapq`)
- Set
- Parent Array
- Distance Array

---

## ▶️ Running the Project

Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
```

Move into the project

```bash
cd your-repository
```

Run

```bash
python main.py
```

---

## 📚 Concepts Covered

- Graph Theory
- Directed Weighted Graphs
- Shortest Path Algorithms
- Greedy Algorithms
- Dynamic Edge Weights
- Priority Queues
- Path Reconstruction
- Negative Cycle Detection
- Delivery Route Optimization

---

## 🎯 Learning Outcomes

This project demonstrates practical implementations of:

- Dijkstra's Algorithm
- Bellman-Ford Algorithm
- Nearest Neighbor Heuristic
- Graph Modeling
- Algorithm Selection Based on Graph Properties

---

## 👨‍💻 Author

**Erfan Moradi and Amirali Pazoki**

Design and Analysis of Algorithms Project