Dynamic Pathfinding Agent
An interactive Python application that visualizes Informed Search Algorithms (A* and Greedy Best-First Search) on a dynamic 2D grid. This project allows users to experiment with different heuristics and grid sizes in real-time.
🚀 Features

* 3-File Architecture: Clean separation between the Environment, Algorithm logic, and GUI.
* Interactive Grid:
  * Select custom Grid Size (Rows x Columns) via an initialization menu.
  * Manual Editor: Left-click to draw walls, Right-click to erase.
  * Random Generator: Generate mazes with 30% obstacle density.


* Search Algorithms:
* **A***: Uses $f(n) = g(n) + h(n)$ to find the optimal path.
* **Greedy Best-First Search**: Uses $f(n) = h(n)$ for faster, though sometimes non-optimal, results.


* **Dual Heuristics**: Toggle between **Manhattan** and **Euclidean** distance formulas.
* **Real-Time Metrics**: Track nodes visited, path cost, and execution time in milliseconds.

## 🛠️ Heuristic Formulas Implemented

The agent calculates its "h-score" using the following mathematical models:

1. **Manhattan Distance**: Used for 4-directional movement.

$$D_{manhattan} = |x_1 - x_2| + |y_1 - y_2|$$


2. **Euclidean Distance**: Represents straight-line distance.

$$D_{euclidean} = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$



## 🎨 Visualization Key

| Color | Meaning |
| --- | --- |
| **Blue (S)** | Start Position |
| **Purple (G)** | Goal Position |
| **Yellow** | **Frontier Nodes**: Currently in the priority queue |
| **Red** | **Visited Nodes**: Already explored by the agent |
| **Green** | **Final Path**: The calculated route to the goal |

## 🎮 Controls

* **[UP/DOWN/LEFT/RIGHT]**: Adjust grid size in the Menu.
* **[ENTER]**: Confirm grid size and start.
* **[SPACE]**: Run the selected search algorithm.
* **[A]**: Toggle between A* and GBFS.
* **[H]**: Toggle between Manhattan and Euclidean heuristics.
* **[G]**: Generate random walls.
* **[C]**: Clear the entire grid and randomize Start/Goal positions.
* **[R]**: Clear only the search path/visuals.
* **[ESC]**: Return to the size selection menu.

## 📂 Project Structure

1. `grid_env.py`: Manages the grid array, walls, and coordinate systems.
2. `algorithms.py`: Contains the A*/GBFS logic and priority queue management.
3. `main.py`: The Pygame-based GUI and user interaction handler.

---

**Would you like me to help you write a "Requirements" section listing the specific versions of Python and Pygame needed to run this?**
