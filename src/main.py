import pygame
import sys
from player import Player
from gameobject import GameObject
from scene import Scene
from block import Block

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# Clock to manage frame rate
clock = pygame.time.Clock()
FPS = 5

# Colors
WHITE = (255, 255, 255)

scene = Scene()
scene.add_object(Player(100, 100))
scene.add_object(Block(100, 500, 200, 50))
scene.add_object(Block(300, 400, 200, 50))
scene.add_object(Block(0, 400, 200, 50))


# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update logic
    scene.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw everything
    scene.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()