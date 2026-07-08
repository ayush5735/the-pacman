import pygame
import time

class PacMan:
    def __init__(self, row, col, tile_size):
        self.row = row
        self.col = col
        self.tile_size = tile_size
        self.direction = (0, 0)
        self.speed = 1.0  # Normal movement speed

        # Reverse-control effect
        self.reverse_active = False
        self.reverse_end_time = 0

    # --- Reverse Control Methods ---
    def start_reverse_controls(self, duration):
        """Enable reversed controls for given duration in seconds."""
        self.reverse_active = True
        self.reverse_end_time = time.time() + duration

    def update_reverse_timer(self):
        """Update reverse timer and disable effect if expired."""
        if self.reverse_active and time.time() > self.reverse_end_time:
            self.reverse_active = False

    def apply_reverse_effect(self, direction):
        """Invert movement direction if reverse mode is active."""
        if self.reverse_active:
            dr, dc = direction
            return (-dr, -dc)
        return direction

    # --- Movement ---
    def move(self, direction, maze, speed):
        """Move Pac-Man in given direction, considering maze walls and speed."""
        # Apply reverse effect if active
        direction = self.apply_reverse_effect(direction)

        dr, dc = direction
        new_row = self.row + int(dr * speed)
        new_col = self.col + int(dc * speed)

        # Check boundaries and walls
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
            if maze[new_row][new_col] != 1:  # Not a wall
                self.row = new_row
                self.col = new_col
                self.direction = direction

    # --- Draw method placeholder ---
    def draw(self, screen, color):
        """Drawing handled by game.py."""
        pass