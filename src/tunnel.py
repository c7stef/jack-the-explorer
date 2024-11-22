import pymunk
import pygame

from block import Solid
from gameobject import GameObject, Named
import collision

class TunnelManager(GameObject, Named):
    def __init__(self):
        self.tunnels = {}
    
    def add_tunnel(self, tunnel, id):
        if id in self.tunnels:
            raise ValueError(f"Tunnel with id {id} already exists")
        self.tunnels[id] = tunnel

    def get_tunnel_by_id(self, id):
        if id not in self.tunnels:
            raise ValueError(f"Tunnel with id {id} does not exist")
        return self.tunnels[id]
    
    @property
    def name(self):
        return 'tunnel_manager'
    
    def update(self):
        pass

    def draw(self, screen):
        pass

class Tunnel(Solid):
    def __init__(self, position, properties):
        width = 50
        height = 100
        super().__init__(position[0], position[1], width, height, pymunk.Body.STATIC, layer=collision.Layer.TUNNEL.value)

        self.upwards = properties['upwards']
        self.tunnel_out_id = properties.get('tunnel_out', None)
        self.id = properties['self_id']

        self.color = (0, 255, 0)
    
    def set_scene(self, scene):
        super().set_scene(scene)
        self.tunnel_manager = self.scene.find_object_by_name('tunnel_manager')
        self.tunnel_manager.add_tunnel(self, self.id)
    
    @property
    def linked_tunnel(self):
        if self.tunnel_out_id is None:
            return None
        return self.tunnel_manager.get_tunnel_by_id(self.tunnel_out_id)

    @property
    def hole_position(self):
        return self.body.position.x, self.body.position.y - self.height / 2 if self.upwards else self.body.position.y + self.height / 2

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

