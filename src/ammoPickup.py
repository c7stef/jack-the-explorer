from solid import Solid
import pygame
import pymunk
import collision

class AmmoPickUp(Solid):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, pymunk.Body.STATIC)
        self.shape.collision_type = collision.Layer.AMMOBOX.value
        self.shape.sensor = True
        self.ammoAmount = 10

    def draw(self, screen):
        pygame.draw.circle(screen, (20, 20, 255), self.scene.relative_position(self.body.position), 25)
