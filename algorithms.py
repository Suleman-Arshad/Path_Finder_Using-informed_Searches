import heapq
import math

class SearchAgent:
    def __init__(self, grid_env):
        self.env = grid_env
    def get_heuristic(self, p1, p2, h_type):
        """
        Calculates distance based on user selection.
        Manhattan: |x1 - x2| + |y1 - y2|
        Euclidean: sqrt((x1 - x2)^2 + (y1 - y2)^2)
        """
        x1, y1 = p1
        x2, y2 = p2
        if h_type == "Manhattan":
            return abs(x1 - x2) + abs(y1 - y2)
        elif h_type == "Euclidean":
            return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return 0

    def get_neighbors(self, node):
        """
        Finds valid adjacent nodes (Up, Down, Left, Right).
        Ensures neighbors are within bounds and not walls.
        """
        r, c = node
        neighbors = []
        # 4-directional movement: Down, Up, Right, Left
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.env.rows and 0 <= nc < self.env.cols:
                if self.env.grid[nr, nc] != 1: # Skip Walls
                    neighbors.append((nr, nc))
        return neighbors

    def run_search(self, algo_type="A*", h_type="Manhattan"):
        start = self.env.start_node
        goal = self.env.goal_node
        
        # Priority Queue: (priority, tie-breaker-counter, current_node)
        frontier_queue = []
        heapq.heappush(frontier_queue, (0, 0, start))
        
        came_from = {start: None}
        g_score = {start: 0} # Cost from start to current node
        
        nodes_visited = 0
        counter = 0 

        while frontier_queue:
            # Pop the node with the lowest f(n)
            current = heapq.heappop(frontier_queue)[2]
            nodes_visited += 1

            # Goal Reached
            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return path, nodes_visited

            # Mark as VISITED (Red - Value 5)
            if current != start:
                self.env.grid[current] = 5

            for neighbor in self.get_neighbors(current):
                new_g = g_score[current] + 1
                
                # If neighbor is new or we found a shorter path
                if neighbor not in g_score or new_g < g_score[neighbor]:
                    g_score[neighbor] = new_g
                    h = self.get_heuristic(neighbor, goal, h_type)
                    
                    # Selection Logic: A* vs GBFS
                    if algo_type == "A*":
                        priority = new_g + h # f(n) = g(n) + h(n)
                    else:
                        priority = h         # f(n) = h(n)
                    
                    counter += 1
                    heapq.heappush(frontier_queue, (priority, counter, neighbor))
                    came_from[neighbor] = current
                    
                    # Mark as FRONTIER (Yellow - Value 6)
                    if neighbor != goal:
                        self.env.grid[neighbor] = 6

        # Return empty path if no solution exists
        return [], nodes_visited

    def reconstruct_path(self, came_from, current):
        
        #Backtracks from Goal to Start and highlights path in Green.
        
        path = []
        while current in came_from:
            path.append(current)
            # Mark as FINAL PATH (Green - Value 4)
            if current != self.env.start_node and current != self.env.goal_node:
                self.env.grid[current] = 4
            current = came_from[current]
        return path[::-1] # Reverse to get Start -> Goal order
