from solid import Solid
import pygame
import pymunk
import collision

class Coin(Solid):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, pymunk.Body.STATIC)
        self.shape.collision_type = collision.Layer.COIN.value
        self.shape.sensor = True

    def draw(self, screen):
        pygame.draw.circle(screen, (220, 220, 30), pygame.Vector2(self.x, self.y), 25)
