import pymunk
import collision
from gameobject import Solid
import pygame
from tilemap import RectangularTile

class WinterTile(RectangularTile):
    def __init__(self, position, image, colliders):
        super().__init__(
            position, image, colliders,
            layer=collision.Layer.BLOCK.value
        )
