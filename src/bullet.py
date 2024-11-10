from solid import Solid
import pygame
import pymunk
import collision
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Bullet(Solid):
    def __init__(self, x, y, directions):
        super().__init__(x, y, 10, 10, pymunk.Body.KINEMATIC)
        self.VELOCITY = 10
        self.shape.collision_type = collision.Layer.BULLET.value
        self.shape.sensor = True
        self.position = pygame.Vector2(x, y)
        self.body.position = self.position.x, self.position.y
        self.ttl = 100

        direction_unit_vectors = {
            Direction.LEFT: pygame.Vector2(-1, 0),
            Direction.RIGHT: pygame.Vector2(1, 0),
            Direction.UP: pygame.Vector2(0, -1),
            Direction.DOWN: pygame.Vector2(0, 1)
        }

        self.direction_vector = pygame.Vector2(0, 0)
        for d in directions:
            self.direction_vector += direction_unit_vectors[d]
        self.direction_vector = self.direction_vector.normalize() * self.VELOCITY

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
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
            self.scene.remove_object(self)

    def draw(self, screen):
        pygame.draw.circle(screen, (250, 100, 30), self.scene.relative_position(self.body.position), 5)
