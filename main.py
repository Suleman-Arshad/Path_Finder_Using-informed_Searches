import pygame
import time
from grid_env import GridEnvironment
from algorithms import SearchAgent

# --- GUI Constants ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)      # Start Node
PURPLE = (128, 0, 128)  # Goal Node
GREEN = (0, 255, 0)     # Final Path
RED = (255, 0, 0)       # Visited Nodes
YELLOW = (255, 255, 0)  # Frontier Nodes
DARK_GRAY = (50, 50, 50)

class Simulation:
    def __init__(self):
        pygame.init()
        self.win_size = 800
        self.sidebar = 250
        self.screen = pygame.display.set_mode((self.win_size + self.sidebar, self.win_size))
        pygame.display.set_caption("Dynamic Pathfinding Agent")
        self.font = pygame.font.SysFont("Arial", 22)
        
        # Grid Selection State
        self.rows = 20
        self.cols = 20
        self.state = "MENU" # MENU or SIMULATION
        
        # Search Settings
        self.algo_type = "A*"
        self.h_type = "Manhattan"
        self.metrics = {"nodes": 0, "time": 0, "cost": 0}

    def draw_menu(self):
        #Initial screen for the user to define grid dimensions.
        self.screen.fill(WHITE)
        title = self.font.render("SELECT GRID SIZE", True, BLACK)
        self.screen.blit(title, (self.win_size // 3, 150))
        
        size_text = self.font.render(f"Rows: {self.rows}  x  Cols: {self.cols}", True, BLUE)
        self.screen.blit(size_text, (self.win_size // 3, 220))
        
        instructions = [
            "Use [UP / DOWN] to change Rows",
            "Use [LEFT / RIGHT] to change Columns",
            "Press [ENTER] to Create Grid"
        ]
        
        for i, text in enumerate(instructions):
            img = self.font.render(text, True, BLACK)
            self.screen.blit(img, (self.win_size // 3, 320 + (i * 40)))

    def draw_ui(self):
        #Real-time metrics dashboard and controls.
        pygame.draw.rect(self.screen, DARK_GRAY, (self.win_size, 0, self.sidebar, self.win_size))
        
        ui_data = [
            f"Grid: {self.rows}x{self.cols}",
            f"Algorithm: {self.algo_type}",
            f"Heuristic: {self.h_type}",
            "",
            "--- METRICS ---",
            f"Nodes Visited: {self.metrics['nodes']}",
            f"Path Cost: {self.metrics['cost']}",
            f"Time: {self.metrics['time']:.2f}ms",
            "",
            "--- CONTROLS ---",
            "[SPACE] Start Search",
            "[A] Toggle A* / GBFS",
            "[H] Toggle Heuristic",
            "[G] Random Walls (30%)",
            "[C] Clear Everything",
            "[R] Clear Path Only",
            "[ESC] Back to Menu"
        ]

        for i, text in enumerate(ui_data):
            surface = self.font.render(text, True, WHITE)
            self.screen.blit(surface, (self.win_size + 20, 40 + (i * 35)))

    def draw_grid(self):
        #Renders nodes and draws 'S' and 'G' labels.
        cell_w = self.win_size // self.cols
        cell_h = self.win_size // self.rows
        
        # Color Map
        colors = {0: WHITE, 1: BLACK, 2: BLUE, 3: PURPLE, 4: GREEN, 5: RED, 6: YELLOW}

        # Create a small font for the letters
        label_font = pygame.font.SysFont("Arial", int(cell_h * 0.8), bold=True)

        for r in range(self.rows):
            for c in range(self.cols):
                val = self.env.grid[r, c]
                color = colors.get(val, WHITE)
                
                # Draw the cell
                rect = (c * cell_w, r * cell_h, cell_w, cell_h)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1) # Border

                # Draw 'S' for Start
                if val == 2:
                    text_surface = label_font.render("S", True, WHITE)
                    # Center the text in the cell
                    text_rect = text_surface.get_rect(center=(c * cell_w + cell_w//2, r * cell_h + cell_h//2))
                    self.screen.blit(text_surface, text_rect)

                # Draw 'G' for Goal
                elif val == 3:
                    text_surface = label_font.render("G", True, WHITE)
                    text_rect = text_surface.get_rect(center=(c * cell_w + cell_w//2, r * cell_h + cell_h//2))
                    self.screen.blit(text_surface, text_rect)

    def main_loop(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if self.state == "MENU":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP: self.rows += 1
                        if event.key == pygame.K_DOWN and self.rows > 5: self.rows -= 1
                        if event.key == pygame.K_RIGHT: self.cols += 1
                        if event.key == pygame.K_LEFT and self.cols > 5: self.cols -= 1
                        if event.key == pygame.K_RETURN:
                            self.env = GridEnvironment(self.rows, self.cols)
                            self.state = "SIMULATION"

                elif self.state == "SIMULATION":
                    # Interactive Map Editor: Add/Remove Walls
                    if pygame.mouse.get_pressed()[0]: # Left Click
                        mx, my = pygame.mouse.get_pos()
                        if mx < self.win_size:
                            r, c = my // (self.win_size // self.rows), mx // (self.win_size // self.cols)
                            self.env.add_wall(r, c)
                    
                    if pygame.mouse.get_pressed()[2]: # Right Click
                        mx, my = pygame.mouse.get_pos()
                        if mx < self.win_size:
                            r, c = my // (self.win_size // self.rows), mx // (self.win_size // self.cols)
                            self.env.remove_wall(r, c)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: self.state = "MENU"
                        if event.key == pygame.K_a: self.algo_type = "GBFS" if self.algo_type == "A*" else "A*"
                        if event.key == pygame.K_h: self.h_type = "Euclidean" if self.h_type == "Manhattan" else "Manhattan"
                        if event.key == pygame.K_g: self.env.generate_random_walls(0.3)
                        if event.key == pygame.K_r: self.env.reset_visuals()
                        if event.key == pygame.K_SPACE:
                            self.env.reset_visuals() # Clear old search first
                            agent = SearchAgent(self.env)
                            start_t = time.perf_counter()
                            path, visited = agent.run_search(self.algo_type, self.h_type)
                            self.metrics["nodes"] = visited
                            self.metrics["time"] = (time.perf_counter() - start_t) * 1000
                            self.metrics["cost"] = len(path) if path else 0
                        if event.key == pygame.K_c: # New key for Clear All
                            self.env.clear_entire_grid()
                            self.metrics = {"nodes": 0, "time": 0, "cost": 0}

            if self.state == "MENU":
                self.draw_menu()
            else:
                self.screen.fill(WHITE)
                self.draw_grid()
                self.draw_ui()

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    sim = Simulation()
    sim.main_loop()
