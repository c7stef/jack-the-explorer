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
        pygame.draw.rect(
            screen, 
            self.color, 
            self.scene.relative_rect(
                pygame.Rect(
                    self.body.position.x - self.width / 2,
                    self.body.position.y - self.height / 2,
                    self.width,
                    self.height
                )
            )
        )

