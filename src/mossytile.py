import pygame
import pymunk

from gameobject import Solid
import collision

class MossyTile(Solid):
    def __init__(self, position, image, colliders):
        self.RADIUS = 10
        
        shapes = []

        width, height = image.get_width(), image.get_height()

        for box in colliders:
            points = [(p.x - width/2, p.y - height/2) for p in box.as_points]

            # Manually offset rectangle points
            points[0] = points[0][0] + self.RADIUS, points[0][1] + self.RADIUS            
            points[1] = points[1][0] + self.RADIUS, points[1][1] - self.RADIUS
            points[2] = points[2][0] - self.RADIUS, points[2][1] - self.RADIUS
            points[3] = points[3][0] - self.RADIUS, points[3][1] + self.RADIUS
            
            shapes.append(pymunk.Poly(None, points, radius=self.RADIUS))

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
