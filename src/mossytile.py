import pygame
import pymunk

from gameobject import GameObject, Solid
import collision
from tilemap import RectangularTile

BG_TINT_COLOR = (69, 139, 170)
FG_TINT_COLOR = (32, 153, 247)
BG_GRADIENT_COLOR1 = (235, 254, 255)
BG_GRADIENT_COLOR2 = (14, 122, 130)

class MossyTile(RectangularTile):
    def __init__(self, position, image, colliders):
        super().__init__(
            position, image, colliders,
            layer=collision.Layer.BLOCK.value
        )