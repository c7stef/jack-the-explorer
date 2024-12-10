import pymunk
import collision
from gameobject import Solid
import pygame
from tilemap import RectangularTile

BG_TINT_COLOR = (192, 215, 226)
FG_TINT_COLOR = (111, 127, 206)
BG_GRADIENT_COLOR1 = (255, 255, 255)
BG_GRADIENT_COLOR2 = (154, 172, 244)

class WinterTile(RectangularTile):
    def __init__(self, position, image, colliders):
        super().__init__(
            position, image, colliders,
            layer=collision.Layer.BLOCK.value
        )
