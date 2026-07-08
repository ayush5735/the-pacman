import pygame
import sys
from game import Game

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 660  # Extra 60 for UI (lives, score)
TILE_SIZE = 30
FPS = 10  # Slower for grid-based feel

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Replica")
clock = pygame.time.Clock()

# Start game
game = Game(screen, TILE_SIZE, FPS)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not game.running:
                game.restart()  # Restart on 'R' after game over/win

    game.update()
    game.draw()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()