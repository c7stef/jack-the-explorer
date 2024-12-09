import pygame
import sys
import pickle

from main_menu import MainMenu
import utils
# Initialize pygame
pygame.init()

# Load controls
try:
    with open("controls.bin", "rb") as f:
        ok = True
        saved_controls = pickle.load(f)
        for key in utils.controls.keys():
            if key not in saved_controls.keys():
                ok = False
                break
        utils.controls = saved_controls if ok else utils.controls
except FileNotFoundError:
    with open("controls.bin", "wb") as f:
        pickle.dump(utils.controls, f)

# Screen settings
if utils.controls['fullscreen']:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((int(utils.controls['resolution'].split("x")[0]), int(utils.controls['resolution'].split("x")[1])))
pygame.display.set_caption("Platformer")

# Clock to manage frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)

main_menu = MainMenu(screen)

utils.current_screen = main_menu

# Main game loop
running = True
while running:
    # Event handling
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    utils.current_screen.send_events(events)

    # Update logic
    utils.current_screen.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw everything
    utils.current_screen.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()
