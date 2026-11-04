# Advanced Search Algorithms & Applications

A collection of clean, production-ready Python implementations for classic search algorithms and state-space exploration problems. This repository covers fundamental graph search techniques (**DFS**, **BFS**, **A* Search**) alongside domain-specific industrial applications such as **Integrated Circuit (IC) Routing**.

---

## 📌 Problem Overview & Algorithm Selection

| # | Problem | Search Algorithm | Primary Characteristics |
|---|---|---|---|
| **1** | **Rat in a Maze** | Depth-First Search (DFS) | Graph traversal, Backtracking, Memory-efficient |
| **2** | **Wolf, Goat, Cabbage** | Breadth-First Search (BFS) | State-space graph, Guarantees shortest path (min steps) |
| **3** | **8-Queens Problem** | DFS + Backtracking | Constraint Satisfaction Problem (CSP), Pruning |
| **4** | **NPC Pathfinding** | A* Heuristic Search | Weighted terrain navigation, Priority Queue, Manhattan Heuristic |
| **5** | **IC Circuit Routing** | Lee's Wavefront Router (BFS) | Electronic Design Automation (EDA), Shortest net path, Obstacle avoidance |

---

## 🔬 Algorithm Deep Dives & Theoretical Formulations

### 1. Rat in a Maze (DFS + Backtracking)
* **Problem Definition**: Find a valid path for a rat navigating from a starting cell $(0, 0)$ to a target destination $(N-1, M-1)$ within an $N \times M$ grid matrix containing impassable obstacles.
* **Mechanism**:
  * The algorithm recursively explores adjacent nodes in four cardinal directions (Up, Down, Left, Right).
  * If a path leads to a dead end (wall or previously visited node), the search **backtracks** by popping the current coordinate off the execution stack and attempting an alternative branch.
* **Complexity**:
  * **Time Complexity**: $\mathcal{O}(4^{N \times M})$ in the worst-case unconstrained grid.
  * **Space Complexity**: $\mathcal{O}(N \times M)$ to store visited states and the recursion call stack.

---

### 2. Wolf, Goat, and Cabbage River Crossing (BFS)
* **Problem Definition**: Transport a farmer, a wolf, a goat, and a cabbage across a river using a boat that holds the farmer and at most one item. The wolf cannot be left alone with the goat, and the goat cannot be left alone with the cabbage.
* **State Space Representation**:
  * State tuple: $S = (F, W, G, C) \in \{0, 1\}^4$, where $0$ represents the left bank and $1$ represents the right bank.
  * Starting State: $(0, 0, 0, 0)$
  * Goal State: $(1, 1, 1, 1)$
* **Safety Constraints**:
  * Wolf & Goat conflict: $(W == G) \land (F \neq W)$
  * Goat & Cabbage conflict: $(G == C) \land (F \neq G)$
* **Why BFS?**: BFS explores all state transitions level-by-level, mathematically guaranteeing that the first path reaching $(1, 1, 1, 1)$ utilizes the minimum number of river trips (7 steps).
* **Complexity**:
  * **Time Complexity**: $\mathcal{O}(|V| + |E|) = \mathcal{O}(2^4 + E) \approx \mathcal{O}(1)$ due to a fixed state space of 16 possible vertices.
  * **Space Complexity**: $\mathcal{O}(|V|)$ for the BFS queue and visited set.

---

### 3. N-Queens Problem (DFS / Backtracking with CSP Pruning)
* **Problem Definition**: Place $N$ non-attacking queens on an $N \times N$ chessboard such that no two queens share the same row, column, or diagonal.
* **Optimization with Set-Based Constraint Tracking**:
  Instead of scanning the grid to evaluate safety at each placement, three lookup sets are maintained for $\mathcal{O}(1)$ conflict verification:
  1. `cols`: Set of occupied column indices $c$.
  2. `diag1` (Main Diagonal): Set of occupied diagonal values $r - c$.
  3. `diag2` (Anti-Diagonal): Set of occupied anti-diagonal values $r + c$.
* **Properties**: For $N = 8$, the search space is pruned from $64^8$ down to $8! = 40,320$ potential configurations, discovering all **92 unique solutions**.
* **Complexity**:
  * **Time Complexity**: $\mathcal{O}(N!)$
  * **Space Complexity**: $\mathcal{O}(N)$ depth recursion stack.

---

### 4. NPC Pathfinding to Player (A* Search)
* **Problem Definition**: Calculate an optimal path for an NPC navigating non-uniform terrain (e.g., roads with cost 1, mud with cost 3, walls impassable) toward a moving player.
* **Evaluation Function**:
  $$f(n) = g(n) + h(n)$$
  * $g(n)$: Exact accumulated cost from the start node to node $n$.
  * $h(n)$: Estimated cost from node $n$ to the goal (Heuristic).
* **Heuristic Choice (Manhattan Distance)**:
  $$h(n) = |x_n - x_{\text{goal}}| + |y_n - y_{\text{goal}}|$$
  Because movements are restricted to four cardinal directions without diagonal steps, Manhattan distance is **admissible** ($h(n) \le h^*(n)$) and **consistent**, ensuring optimal pathfinding.
* **Complexity**:
  * **Time Complexity**: $\mathcal{O}(|E| \log |V|)$ using a Min-Heap priority queue (`heapq`).
  * **Space Complexity**: $\mathcal{O}(|V|)$ to maintain open and closed sets.

---

### 5. IC Circuit Routing (Lee's Algorithm & EDA Routing Frameworks)

In Very Large Scale Integration (VLSI) and Printed Circuit Board (PCB) physical design, **routing** connects electronic pins with physical conductive traces while obeying spacing rules and avoiding blockages.

#### Implemented Algorithm: Lee's Maze Router (Wavefront Expansion)
1. **Wavefront Propagation**: Performs a BFS expansion centered at source Pin A. Neighboring unvisited grid cells increment distance labels ($1, 2, 3, \dots, d$) until target Pin B is encountered.
2. **Backtracking / Retrace**: Traces backward from Pin B to Pin A by selecting adjacent cells with strictly decreasing values ($d-1, d-2, \dots, 0$).
3. **Obstacle Reservation**: The routed path is locked in the grid with a unique `Net_ID`, acting as a permanent barrier for subsequent net routing operations.

#### Advanced Routing Methods in EDA (Comparative Overview)
* **Hadlock's Algorithm (Detour Router)**:
  * Enhances Lee's Router by assigning cost based on **detour steps** (moving away from target pin) rather than total distance.
  * Reduces search space drastically using A*-like priority queues.
* **Line-Search Routers (Mikami-Tabuchi & Hightower Algorithms)**:
  * Avoids memory-intensive grid discretization by firing horizontal and vertical line segments from pins.
  * Routers find intersections among line segments to form connections.
* **Multi-Layer Negotiated Congestion Routing (Pathfinder Algorithm)**:
  * Used in modern FPGAs and ICs. Allows nets to temporarily share routing resources (over-use), then iteratively applies congestion penalties ($\text{Cost} = \text{BaseCost} + \text{Penalty}$) until all overlaps are eliminated.

---

## 💻 Project Structure & File Index

```
.
├── search_algorithms.py   # Complete, runnable Python module containing all 5 algorithms
└── README.md              # Documentation and mathematical formulation
```

---

## ⚡ Execution Guide

### Prerequisites
* Python 3.7 or higher (No third-party dependencies required; uses standard libraries `dataclasses`, `heapq`, `collections`, `typing`).

### Running the Code
Execute the Python module directly to view ASCII visualizations and textual trace outputs for all five problems:

```bash
python search_algorithms.py
```