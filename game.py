import pygame
import random
import time
from entities.pacman import PacMan
from entities.ghost import RedGhost, YellowGhost, WhiteGhost
from utils.maze import MAZE_LAYOUT, count_dots

class Game:
    def __init__(self, screen, tile_size, fps):
        self.screen = screen
        self.tile_size = tile_size
        self.fps = fps
        self.rows = len(MAZE_LAYOUT)
        self.cols = len(MAZE_LAYOUT[0])
        self.maze = MAZE_LAYOUT
        self.dots = count_dots(self.maze)
        self.dots_eaten = 0
        self.lives = 3
        self.running = True
        self.game_over = False
        self.win = False

        # Effects
        self.slow_timer = 0
        self.slow_end_time = 0

        # Visibility effect
        self.visibility_timer = 0
        self.visibility_end_time = 0
        self.visibility_radius = 100  # pixels around Pac-Man

        # Initialize Pac-Man
        start_row, start_col = 10, 10
        self.pacman = PacMan(start_row, start_col, tile_size)

        # Ghosts
        self.red_ghost = RedGhost(1, 1, tile_size)
        self.yellow_ghost = YellowGhost(15, 15, tile_size)
        self.white_ghost = WhiteGhost(5, 5, tile_size)

        # Yellow ghost patrol area
        self.yellow_patrol_area = (15, 20, 15, 20)

        # Colors
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.GRAY = (128, 128, 128)

    def restart(self):
        self.__init__(self.screen, self.tile_size, self.fps)

    def update(self):
        if not self.running:
            return

        # Update reverse-control timer
        self.pacman.update_reverse_timer()

        # Input
        keys = pygame.key.get_pressed()
        direction = None
        if keys[pygame.K_UP]: direction = (-1, 0)
        elif keys[pygame.K_DOWN]: direction = (1, 0)
        elif keys[pygame.K_LEFT]: direction = (0, -1)
        elif keys[pygame.K_RIGHT]: direction = (0, 1)

        # Reverse-direction patch
        if direction:
            direction = self.pacman.apply_reverse_effect(direction)

            speed = 1 if self.slow_timer <= 0 else 0.5
            self.pacman.move(direction, self.maze, speed)

        # Eat dot
        if self.maze[self.pacman.row][self.pacman.col] == 0:
            self.maze[self.pacman.row][self.pacman.col] = 2
            self.dots_eaten += 1
            if self.dots_eaten >= self.dots:
                self.win = True
                self.running = False

        # Ghost updates
        self.red_ghost.chase(self.pacman.row, self.pacman.col, self.maze)
        self.yellow_ghost.patrol(self.yellow_patrol_area, self.maze, self.pacman)
        self.white_ghost.random_move(self.maze)

        # Collisions
        self.check_collisions()

        # Timers
        now = time.time()

        # Slow effect
        if self.slow_timer > 0 and now > self.slow_end_time:
            self.slow_timer = 0

        # Visibility effect
        if self.visibility_timer > 0 and now > self.visibility_end_time:
            self.visibility_timer = 0

        if self.win or self.lives <= 0:
            self.running = False
            self.game_over = self.lives <= 0

    def check_collisions(self):
        # RED → Lose life
        if (self.pacman.row, self.pacman.col) == (self.red_ghost.row, self.red_ghost.col):
            self.lives -= 1
            self.respawn()

        # WHITE → Slow movement
        if (self.pacman.row, self.pacman.col) == (self.white_ghost.row, self.white_ghost.col):
            self.slow_timer = 5
            self.slow_end_time = time.time() + 5

        # YELLOW → Reverse controls
        if (self.pacman.row, self.pacman.col) == (self.yellow_ghost.row, self.yellow_ghost.col):
            self.pacman.start_reverse_controls(3)  # 3 seconds reverse control

    def respawn(self):
        start_row, start_col = 10, 10
        self.pacman = PacMan(start_row, start_col, self.tile_size)
        self.red_ghost = RedGhost(1, 1, self.tile_size)
        self.yellow_ghost = YellowGhost(15, 15, self.tile_size)
        self.white_ghost = WhiteGhost(5, 5, self.tile_size)

    def draw(self):
        self.screen.fill(self.BLACK)

        # Draw maze
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.tile_size
                y = row * self.tile_size
                if self.maze[row][col] == 1:
                    pygame.draw.rect(self.screen, self.BLUE, (x, y, self.tile_size, self.tile_size))
                elif self.maze[row][col] == 0:
                    pygame.draw.circle(self.screen, self.WHITE, (x + self.tile_size//2, y + self.tile_size//2), 3)

        # Draw entities
        self.draw_entity(self.pacman, self.YELLOW)
        self.draw_entity(self.red_ghost, self.RED)
        self.draw_entity(self.yellow_ghost, self.ORANGE)
        self.draw_entity(self.white_ghost, self.GRAY)

        # --- Low visibility overlay ---
        if self.visibility_timer > 0:
            overlay = pygame.Surface((self.cols * self.tile_size, self.rows * self.tile_size))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(210)

            px = self.pacman.col * self.tile_size + self.tile_size//2
            py = self.pacman.row * self.tile_size + self.tile_size//2
            pygame.draw.circle(overlay, (0, 0, 0, 0), (px, py), self.visibility_radius)

            self.screen.blit(overlay, (0, 0))

        # UI
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {self.lives}", True, self.WHITE)
        dots_text = font.render(f"Dots: {self.dots_eaten}/{self.dots}", True, self.WHITE)
        self.screen.blit(lives_text, (10, self.rows * self.tile_size + 10))
        self.screen.blit(dots_text, (200, self.rows * self.tile_size + 10))

        # Game end screen
        if not self.running:
            over_font = pygame.font.Font(None, 48)
            if self.win:
                text = over_font.render("You Win! Press R to restart", True, self.WHITE)
            else:
                text = over_font.render("Game Over! Press R to restart", True, self.WHITE)
            text_rect = text.get_rect(center=(self.cols * self.tile_size // 2, self.rows * self.tile_size + 30))
            self.screen.blit(text, text_rect)

    def draw_entity(self, entity, color):
        x = entity.col * self.tile_size
        y = entity.row * self.tile_size
        pygame.draw.circle(self.screen, color, (x + self.tile_size//2, y + self.tile_size//2), self.tile_size//2 - 2)

print("Game loaded!")