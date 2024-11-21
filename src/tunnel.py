import pymunk
import pygame

from block import Solid
import collision



class Tunnel(Solid):
    def __init__(self, x, y, width, height, linked_tunnel):
        super().__init__(x, y, width, height, pymunk.Body.STATIC, layer=collision.Layer.TUNNEL.value)
        self.linked_tunnel = linked_tunnel
        self.color = (0, 255, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 100), self.scene.relative_rect(pygame.Rect(self.body.position, (self.width, self.height))))

