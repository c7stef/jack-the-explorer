import pymunk
import pygame

from block import Solid
import collision



class Tunnel(Solid):
    def __init__(self, position, properties, upwards=False):
        width = 50
        height = 100
        super().__init__(position[0], position[1], width, height, pymunk.Body.STATIC, layer=collision.Layer.TUNNEL.value)

        self.upwards = upwards
        if 'tunnel_out' in properties:
            self.linked_tunnel = properties['tunnel_out']
        else:
            self.linked_tunnel = None
        if 'upwards' in properties:
            upwards = properties['upwards']
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

