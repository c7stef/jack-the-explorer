from gameobject import GameObject
import collision
import pygame

import numpy as np

# Example of another game object class (e.g., a simple block)
class Block(GameObject):
    def __init__(self, x, y, width, height):
        self.layer = collision.Layer.BLOCK
        self.rect = pygame.Rect(x, y, width, height)
        self.position = pygame.Vector2(x, y)
        self.top = pygame.Rect(x, y, width, 1)

    def printPosition(self):
        print("Block data:")
        print(self.position)
        print(self.rect)
        print("Left px: " + str(self.rect.left))

    def update(self):
        # Block logic can go here, if needed
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), self.rect)  # Drawing a brown block
