from solid import Solid
import pygame
import pymunk
import collision

class Block(Solid):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, pymunk.Body.STATIC)
        self.shape.collision_type = collision.Layer.BLOCK.value

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(self.body.position.x - self.rect.w / 2, self.body.position.y - self.rect.h / 2, self.rect.width, self.rect.height))  # Drawing a brown block
    