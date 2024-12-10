import pygame
import pymunk

from gameobject import Solid, GameObject
import collision
import utils
import math

player_bullet_sprite = pygame.image.load("assets/bullet/player_bullet.png")

class BulletBlast(GameObject):
    def __init__(self, x, y):
        self.LIFETIME = 10
        self.progress = 0
        self.position = pygame.Vector2(x, y)
        self.circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    
    def update(self):
        self.progress += 1
        if self.progress >= self.LIFETIME:
            self.scene.remove_object(self)

    def draw(self, screen):
        self.circle_surface.fill((0, 0, 0, 0))

        pygame.draw.circle(
            self.circle_surface,
            (200, 230, 255, 200 * (1 - self.progress / self.LIFETIME)),
            self.circle_surface.get_rect().center,
            80 * self.progress / self.LIFETIME
        )
        
        screen.blit(
            self.circle_surface,
            self.scene.relative_position(
                self.position - pygame.Vector2(self.circle_surface.get_rect().size) / 2
            )
        )

class Bullet(Solid):
    def __init__(self, x, y, directions):
        super().__init__(x, y, 20, 20,
                         body_type=pymunk.Body.KINEMATIC,
                         layer=collision.Layer.BULLET.value)
        self.VELOCITY = 15
        self.shape.sensor = True
        self.position = pygame.Vector2(x, y)
        self.body.position = self.position.x, self.position.y
        self.ttl = 80
        self.direction_vector = directions.normalize() * self.VELOCITY
        angle = math.degrees(math.atan2(-self.direction_vector.y, self.direction_vector.x))
        self.image = pygame.transform.rotate(player_bullet_sprite, angle)
        self.rotated_rect = self.image.get_rect(center=pygame.Vector2(x, y))

    def update(self):
        self.ttl -= 1
        if self.ttl < 0:
            self.scene.remove_object(self)
            return

        self.position += self.direction_vector
        self.body.position = self.position.x, self.position.y

        collisions = self.get_collisions()

        set_to_die = False
        for collision_data in collisions:
            if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                self.scene.find_rigid_body(collision_data["shape"]).deal_damage(1)
            
            set_to_die = True
            
        if set_to_die:
            self.scene.add_object(BulletBlast(self.body.position.x, self.body.position.y))
            self.scene.remove_object(self)

    def draw(self, screen):
        screen.blit(self.image, self.scene.relative_position(pygame.Vector2(self.body.position) - pygame.Vector2(self.rotated_rect.size) / 2))

class EnemyBullet(Bullet):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.shape.collision_type = collision.Layer.ENEMYBULLET.value

    def update(self):
        self.ttl -= 1
        if self.ttl < 0:
            self.scene.remove_object(self)
            return

        self.position += self.direction_vector
        self.body.position = self.position.x, self.position.y

        collisions = self.get_collisions()

        set_to_die = False
        for collision_data in collisions:
            if collision_data["shape"].collision_type == collision.Layer.PLAYER.value:
                self.scene.find_rigid_body(collision_data["shape"]).deal_damage(1)
            
            set_to_die = True

        if set_to_die:
            self.scene.remove_object(self)