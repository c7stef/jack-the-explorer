import pygame
import pymunk

from gameobject import Solid
import collision

class MossyTile(Solid):
    def __init__(self, position, image, colliders):
        super().__init__(
            position.x, position.y,
            image.get_width(), image.get_height(),
            body_type=pymunk.Body.STATIC,
            layer=collision.Layer.BLOCK.value
        )
        self.image = image

    def body_data(self):
        return (self.body, self.shape)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.scene.relative_position((self.body.position.x - self.width / 2, self.body.position.y - self.height / 2)))
