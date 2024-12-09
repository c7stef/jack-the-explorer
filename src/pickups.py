import pymunk
import pygame

from block import Solid
import collision

coin_sprite = pygame.image.load('assets/coin/coin.png')
health_sprite = pygame.image.load('assets/heart/pickup.png')
ammo_sprite = pygame.image.load('assets/bullet/ammo.png')

class AmmoPickUp(Solid):
    def __init__(self, position, properties):
        super().__init__(position.x, position.y, 54, 54,
                         body_type=pymunk.Body.STATIC,
                         layer=collision.Layer.AMMOBOX.value)
        self.shape.sensor = True
        self.ammo_amount = properties.get('bullet_capacity', 10)

    def draw(self, screen):
        screen.blit(ammo_sprite, self.scene.relative_position((self.body.position.x - 40, self.body.position.y - 40)))


class Coin(Solid):
    def __init__(self, position, properties):
        super().__init__(position.x, position.y, 54, 54,
                         body_type=pymunk.Body.KINEMATIC,
                         layer=collision.Layer.COIN.value)
        self.shape.sensor = True

    def draw(self, screen):
        screen.blit(coin_sprite, self.scene.relative_position((self.body.position.x - 40, self.body.position.y - 40)))

class HealthPickUp(Solid):
    def __init__(self, position, properties):
        super().__init__(position.x, position.y, 54, 54, pymunk.Body.STATIC)
        self.shape.collision_type = collision.Layer.HEALTHBOX.value
        self.shape.sensor = True
        self.health_amount = properties.get('health', 5)

    def draw(self, screen):
        screen.blit(health_sprite, self.scene.relative_position((
            self.body.position.x - health_sprite.get_width()/2,
            self.body.position.y - health_sprite.get_width()/2)
        ))
