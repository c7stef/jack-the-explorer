import pymunk
import pygame

from block import Solid
import collision
import random
import math

coin_sprite = pygame.image.load('assets/coin/coin.png')
health_sprite = pygame.image.load('assets/heart/pickup.png')
ammo_sprite = pygame.image.load('assets/bullet/ammo.png')

class PickUp(Solid):
    def __init__(self, position, box_size, sprite, layer):
        super().__init__(position.x, position.y, box_size.x, box_size.y,
                         body_type=pymunk.Body.KINEMATIC,
                         layer=layer)
        self.sprite = sprite
        self.initial_position = position
        self.shape.sensor = True
        self.wave_time = (math.pi / 1.5) * random.randrange(0, 100) / 100
        self.WAVE_AMPLITUDE = 7
    
    def update(self):
        self.wave_time += 0.05
        self.body.position = (
            self.initial_position.x,
            self.initial_position.y + math.sin(self.wave_time) * self.WAVE_AMPLITUDE
        )
    
    def draw(self, screen):
        screen.blit(self.sprite, self.scene.relative_position((
            self.body.position.x - self.sprite.get_width() / 2,
            self.body.position.y - self.sprite.get_height() / 2
        )))

class AmmoPickUp(PickUp):
    def __init__(self, position, properties):
        super().__init__(
            position,
            pygame.Vector2(54, 54),
            ammo_sprite,
            layer=collision.Layer.AMMOBOX.value
        )

        self.ammo_amount = properties.get('bullet_capacity', 10)

class Coin(PickUp):
    def __init__(self, position, properties):
        super().__init__(
            position,
            pygame.Vector2(54, 54),
            coin_sprite,
            layer=collision.Layer.COIN.value
        )

class HealthPickUp(PickUp):
    def __init__(self, position, properties):
        super().__init__(
            position,
            pygame.Vector2(54, 54),
            health_sprite,
            layer=collision.Layer.HEALTHBOX.value
        )
        self.health_amount = properties.get('health', 5)
