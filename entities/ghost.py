import random
import math

class BaseGhost:
    def __init__(self, row, col, tile_size):
        self.row = row
        self.col = col
        self.tile_size = tile_size
        self.direction = (0, 0)

    def is_valid_move(self, new_row, new_col, maze):
        rows, cols = len(maze), len(maze[0])
        return (0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] != 1)

    def move(self, direction, maze):
        dr, dc = direction
        new_row = self.row + dr
        new_col = self.col + dc
        if self.is_valid_move(new_row, new_col, maze):
            self.row = new_row
            self.col = new_col
            self.direction = direction
        else:
            self.direction = (-dr, -dc) if random.random() > 0.5 else (dr, -dc)

    # --- FIX ADDED HERE ---
    def random_move(self, maze):
        """Basic random movement available to all ghosts."""
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            if self.is_valid_move(nr, nc, maze):
                self.move((dr, dc), maze)
                return
    # -----------------------


class RedGhost(BaseGhost):
    def __init__(self, row, col, tile_size):
        super().__init__(row, col, tile_size)
        self.speed_delay = 2
        self.tick = 0

    def chase(self, target_row, target_col, maze):
        self.tick += 1
        if self.tick % self.speed_delay != 0:
            return

        dr = 1 if target_row > self.row else -1 if target_row < self.row else 0
        dc = 1 if target_col > self.col else -1 if target_col < self.col else 0

        if abs(target_row - self.row) > abs(target_col - self.col):
            options = [(dr, 0), (0, dc)]
        else:
            options = [(0, dc), (dr, 0)]

        for direction in options:
            nr = self.row + direction[0]
            nc = self.col + direction[1]
            if self.is_valid_move(nr, nc, maze):
                self.move(direction, maze)
                return

        self.random_move(maze)  # now safe

class YellowGhost(BaseGhost):
    def patrol(self, area, maze, pacman):
        min_row, max_row, min_col, max_col = area
        dr, dc = self.direction

        # Move horizontally, bounce at edges
        new_col = self.col + dc
        if not (min_col <= new_col <= max_col) or not self.is_valid_move(self.row, new_col, maze):
            dc = -dc

        # Occasionally move row
        if random.random() < 0.1:
            new_row = self.row + (1 if random.random() > 0.5 else -1)
            if min_row <= new_row <= max_row and self.is_valid_move(new_row, self.col, maze):
                self.row = new_row
                dr = 0

        # Move ghost
        self.move((dr, dc), maze)
        self.direction = (dr, dc)

        # Reverse controls effect
        if (self.row, self.col) == (pacman.row, pacman.col):
            pacman.start_reverse_controls(3)  # 3 seconds reverse controls


class WhiteGhost(BaseGhost):
    def random_move(self, maze):
        if random.random() < 0.3:
            directions = [(0,1), (0,-1), (1,0), (-1,0)]
            self.direction = random.choice(directions)

        self.move(self.direction, maze)