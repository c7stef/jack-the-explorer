import pygame
import pymunk

from collision import Layer

from gameobject import Solid, Named

from utils import scale_surface

flag = pygame.image.load("assets/checkpoint/flag.png")

class Checkpoint(Solid, Named):
    def __init__(self, position, properties=None):
        super().__init__(position.x, position.y, 50, 50,
        body_type=pymunk.Body.STATIC, layer=Layer.CHECKPOINT.value)
        self.shape.sensor = True

        if properties:
            if 'order' in properties:
                self.order = properties['order']

        self.flag = scale_surface(flag, (50, 50))
        self.color = (200, 50, 0)
        self.reachedColor = (10, 125, 15)
        self.notReachedColor = (200, 50, 0)
        self.radius = 0

    def update(self):
        self.radius += 0.5
        if self.radius >= 20:
            self.radius = 0

    def draw(self, screen):
        screen.blit(self.flag, self.scene.relative_position(self.body.position) - pygame.Vector2(25, 25))
        circleCenter = self.scene.relative_position(self.body.position)
        circleCenter = (circleCenter.x + 18, circleCenter.y - 9)
        pygame.draw.circle(screen, self.color, circleCenter, self.radius, 2)

    def reached(self, player):
        if player.lastCheckpoint:
            if self.order != player.lastCheckpoint.order + 1:
                return player.lastCheckpoint
            else:
                self.color = self.reachedColor
                player.lastCheckpoint = self
                return self
        elif self.order == 0:
            self.color = self.reachedColor
            player.lastCheckpoint = self
            return self
        return None

    def reset(self):
        self.color = self.notReachedColor

    @property
    def name(self):
        return "Checkpoint"
