import pygame
import pymunk
from solid import Solid

class MossyTile(Solid):
    def __init__(self, position, image, colliders):
        super(position.x, position.y, image.width, image.height, pymunk.Body.STATIC)
        self.image = image
        

    def body_data(self):

    def update(self):
        pass

    def draw(self, screen):
        pass
