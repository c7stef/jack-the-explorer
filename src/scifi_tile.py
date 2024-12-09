import pymunk
import collision
from gameobject import Solid
import pygame

class SciFiTile(Solid):
    def __init__(self, position, image, colliders):
        self.CORNER_RADIUS = 5
        self.z_index = 1
        
        shapes = []

        width, height = image.get_width(), image.get_height()

        if colliders == []:
            shapes.append(pymunk.Poly.create_box(None, (56, 56), radius=self.CORNER_RADIUS))
        else:
            for poly in colliders:
                points = [(x - width/2, y - height/2) for x, y in poly.apply_transformations()]
                points = [(x * 0.85, y * 0.85) for x, y in points]
                
                shapes.append(pymunk.Poly(None, points, radius=self.CORNER_RADIUS))

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
