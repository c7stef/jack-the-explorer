import pymunk
import pygame

from block import Solid
import collision

class AmmoPickUp(Solid):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, pymunk.Body.STATIC)
        self.shape.collision_type = collision.Layer.AMMOBOX.value
        self.shape.sensor = True
        self.ammoAmount = 10

    def draw(self, screen):
        pygame.draw.circle(screen, (20, 20, 255), self.scene.relative_position(self.body.position), 25)


class Coin(Solid):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, pymunk.Body.STATIC)
        self.shape.collision_type = collision.Layer.COIN.value
        self.shape.sensor = True

    def draw(self, screen):
        pygame.draw.circle(screen, (220, 220, 30), self.scene.relative_position(self.body.position), 25)
