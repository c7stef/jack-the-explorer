import pymunk
import collision
from gameobject import GameObject
import pygame
from tilemap import SolidTile

BG_TINT_COLOR = (29, 28, 70)
FG_TINT_COLOR = (60, 115, 24)
BG_GRADIENT_COLOR1 = (122, 115, 140)
BG_GRADIENT_COLOR2 = (58, 49, 79)

class SciFiTile(SolidTile):
    def __init__(self, position, image, colliders):
        super().__init__(
            position, image, colliders,
            layer=collision.Layer.BLOCK.value
        )
