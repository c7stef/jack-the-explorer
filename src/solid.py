from gameobject import GameObject
import collision
import pygame
import pymunk
from rigidbody import RigidBody

class Solid(GameObject, RigidBody):
    def __init__(self, x, y, width, height, body_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.position = pygame.Vector2(x, y)

        self.moment = pymunk.moment_for_box(mass=10, size=(width, height))
        self.body = pymunk.Body(mass=10, moment=self.moment, body_type=body_type)
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, size=(width, height))

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def body_data(self):
        return (self.body, self.shape)

    def update(self):
        pass

    def draw(self, screen):
        pass

