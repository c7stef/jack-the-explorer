import pygame
import pymunk
import math

from gameobject import Solid
import collision
import utils

class Block(Solid):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height,
                         body_type=pymunk.Body.STATIC)

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))


class DecayingBlock(Solid):
    def __init__(self, x, y, width, height, ttl):
        super().__init__(x, y, width, height,
                         body_type=pymunk.Body.STATIC,
                         layer=collision.Layer.DECBLOCK.value)

        self.color = (139, 69, 19)
        self.ttl = ttl

    def update(self):
        if self.ttl < 0:
            self.scene.remove_object(self)

    def decay(self):
        self.ttl -= 1
        self.color = (
            max(self.color[0] - 1, 0),
            max(self.color[1] - 1, 0),
            max(self.color[2] - 1, 0)
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))


class MovingPlatform(Solid):
    def __init__(self, width, height, p1, p2, speed):
        super().__init__(p1.x, p1.y, width, height,
                         body_type=pymunk.Body.KINEMATIC,
                         layer=collision.Layer.PLATFORM.value)
        self.p1 = p1
        self.p2 = p2
        self.forward = True
        self.speed_vector = pygame.Vector2.normalize(p2 - p1) * speed

    def update(self):
        if math.fabs(self.p1.x - self.p2.x) < utils.EPSILON:
            t = (self.body.position.y - self.p1.y) / (self.p2.y - self.p1.y)
        else:
            t = (self.body.position.x - self.p1.x) / (self.p2.x - self.p1.x)

        if t > 1:
            self.forward = False
        if t < 0:
            self.forward = True

        final_velocity = self.speed_vector if self.forward else -self.speed_vector
        self.body.velocity = (final_velocity.x, final_velocity.y)

    def draw(self, screen):
        pygame.draw.rect(screen, (60, 200, 200), self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))


class Spike(Solid):
    def __init__(self, position, properties=None):
        super().__init__(position.x, position.y, properties['width'], properties['height'],
                         body_type=pymunk.Body.STATIC, layer=collision.Layer.SPIKE.value)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))