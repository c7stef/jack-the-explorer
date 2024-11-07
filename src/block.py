from gameobject import GameObject
import collision
import pygame
import pymunk
from rigidbody import RigidBody

import numpy as np

# Example of another game object class (e.g., a simple block)
class Block(GameObject, RigidBody):
    def __init__(self, x, y, width, height):
        self.layer = collision.Layer.BLOCK
        self.rect = pygame.Rect(x, y, width, height)
        self.position = pygame.Vector2(x, y)
        self.top = pygame.Rect(x, y, width, 1)

        self.moment = pymunk.moment_for_box(mass=0, size=(width, height))
        self.body = pymunk.Body(mass=0, moment=self.moment, body_type=pymunk.Body.STATIC)
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, size=(width, height))
        self.shape.friction = 0.8
        self.shape.collision_type = collision.Layer.BLOCK.value

    def body_data(self):
        return (self.body, self.shape)

    def update(self):
        # Block logic can go here, if needed
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(self.body.position.x - self.rect.w / 2, self.body.position.y - self.rect.h / 2, self.rect.width, self.rect.height))  # Drawing a brown block
