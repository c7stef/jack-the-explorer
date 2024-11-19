from enum import Enum

from PIL import Image
import pygame

EPSILON = 0.001

escapePressed = False

currentScreen = None
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

def load_gif(path, scale=None):
    image = Image.open(path)
    frames = []
    while True:
        try:
            frame = image.copy().convert("RGBA")
            pygameFormatImage = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            if scale:
                pygameFormatImage = pygame.transform.scale(pygameFormatImage, scale)
            frames.append(pygameFormatImage)
            image.seek(image.tell() + 1)
        except EOFError:
            break
    return frames