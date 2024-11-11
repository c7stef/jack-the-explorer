import pygame
import sys
from player import Player
from gameobject import GameObject
from scene import Scene
from block import Block
from movingplatform import MovingPlatform
from enemy import Enemy
from coin import Coin
from decayingBlock import DecayingBlock

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# Clock to manage frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)

scene = Scene(screen)
scene.add_object(Player(100, 100))
scene.add_object(Block(300, 500, 200, 50))
scene.add_object(Block(500, 400, 200, 50))
scene.add_object(Block(200, 400, 200, 50))
scene.add_object(MovingPlatform(200, 50, pygame.Vector2(100, 200), pygame.Vector2(300, 200), 10))
scene.add_object(Enemy(pygame.Vector2(250, 450), pygame.Vector2(350, 450), 2))
scene.add_object(Coin(600, 350))
scene.add_object(DecayingBlock(150, 150, 1000, 10, 100))

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