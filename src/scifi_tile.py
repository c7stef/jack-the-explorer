import pymunk
import collision
from gameobject import Solid
import pygame

class SciFiTile(Solid):
    def __init__(self, position, image, colliders):
        self.CORNER_RADIUS = 10
        self.z_index = 1
        
        shapes = []

        width, height = image.get_width(), image.get_height()
        shapes.append(pymunk.Poly.create_box(None, (118, 118), radius=self.CORNER_RADIUS))

        super().__init__(
            position.x, position.y,
            width, height,
            layer=collision.Layer.BLOCK.value,
            shapes=shapes
        )

        self.image = image
        for shape in self.shapes:
            shape.body = self.body

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.scene.relative_position((self.body.position.x - self.width / 2, self.body.position.y - self.height / 2)))
