import pygame
import sys

from mainMenu import MainMenu
import utils
# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# Clock to manage frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)

mainMenu = MainMenu(screen)

utils.currentScreen = mainMenu

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update logic
    utils.currentScreen.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw everything
    utils.currentScreen.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()
