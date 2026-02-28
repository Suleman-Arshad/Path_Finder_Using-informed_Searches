import numpy as np
import random

class GridEnvironment:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # 0: Empty (White), 1: Wall (Black), 2: Start (Blue), 
        # 3: Goal (Purple), 4: Path (Green), 5: Visited (Red), 6: Frontier (Yellow)
        self.grid = np.zeros((rows, cols))
        # Set fixed Start and Goal positions
        self.start_node = (1, 1)
        self.goal_node = (rows - 2, cols - 2)
        # Place them on the grid immediately
        self.randomize_endpoints()
        self.place_endpoints()
    def randomize_endpoints(self):
        # Pick a random row and column within bounds
        self.start_node = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        
        self.goal_node = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        
        # Ensure Start and Goal are not at the same location
        while self.goal_node == self.start_node:
            self.goal_node = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        
        self.place_endpoints()
    def place_endpoints(self):
        self.grid[self.start_node] = 2
        self.grid[self.goal_node] = 3

    def generate_random_walls(self, density=0.3):
        #Generates a maze with a user-defined obstacle density.
        for r in range(self.rows):
            for c in range(self.cols):
                # Skip the Start and Goal nodes so they remain accessible
                if (r, c) == self.start_node or (r, c) == self.goal_node:
                    continue
                # Use random probability to decide if a cell is a wall
                if random.random() < density:
                    self.grid[r, c] = 1
                else:
                    self.grid[r, c] = 0
        self.place_endpoints()
    def clear_entire_grid(self):
        self.grid = np.zeros((self.rows, self.cols))
        self.place_endpoints()

    def add_wall(self, row, col):
        #Allows manual placement of obstacles via the Interactive Map Editor.
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if (row, col) != self.start_node and (row, col) != self.goal_node:
                self.grid[row, col] = 1

    def remove_wall(self, row, col):
        #Allows manual removal of obstacles.
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if (row, col) != self.start_node and (row, col) != self.goal_node:
                self.grid[row, col] = 0

    def reset_visuals(self):
        #Clears path, visited, and frontier nodes without removing walls.
        for r in range(self.rows):
            for c in range(self.cols):
                # If the cell is Path (4), Visited (5), or Frontier (6), reset to Empty (0)
                if self.grid[r, c] in [4, 5, 6]:
                    self.grid[r, c] = 0
        self.place_endpoints()
