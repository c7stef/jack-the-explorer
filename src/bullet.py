import pygame
import pymunk

from gameobject import Solid
import collision
import utils

class Bullet(Solid):
    def __init__(self, x, y, directions):
        super().__init__(x, y, 10, 10, pymunk.Body.KINEMATIC)
        self.VELOCITY = 15
        self.shape.collision_type = collision.Layer.BULLET.value
        self.shape.sensor = True
        self.position = pygame.Vector2(x, y)
        self.body.position = self.position.x, self.position.y
        self.ttl = 80
        self.direction_vector = directions.normalize() * self.VELOCITY

    def update(self):
        self.ttl -= 1
        if self.ttl < 0:
            self.scene.remove_object(self)

        self.position += self.direction_vector
        self.body.position = self.position.x, self.position.y

        collisions = self.get_collisions()

        for collision_data in collisions:
            # Add more things to ignore collision with
            if collision_data["shape"].collision_type == collision.Layer.COIN.value:
                continue
            if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                self.scene.find_rigid_body(collision_data["shape"]).deal_damage(1)
            self.scene.remove_object(self)

    def draw(self, screen):
        pygame.draw.circle(screen, (250, 100, 30), self.scene.relative_position(self.body.position), 5)


class EnemyBullet(Bullet):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.shape.collision_type = collision.Layer.ENEMYBULLET.value

    def update(self):
        self.ttl -= 1
        if self.ttl < 0:
            self.scene.remove_object(self)

        self.position += self.direction_vector
        self.body.position = self.position.x, self.position.y

        collisions = self.get_collisions()

        for collision_data in collisions:
            # Add more things to ignore collision with
            if collision_data["shape"].collision_type == collision.Layer.COIN.value:
                continue
            if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                self.scene.find_rigid_body(collision_data["shape"]).deal_damage(1)
            self.scene.remove_object(self)