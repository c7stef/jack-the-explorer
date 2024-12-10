import pygame
import pymunk

from gameobject import Solid
from tilemap import SolidTile
from bullet import EnemyBullet
import collision
import utils

class Enemy(Solid):
    def __init__(self, position, properties):
        super().__init__(position.x, position.y, 50, 50,
                         body_type=pymunk.Body.KINEMATIC,
                         layer=collision.Layer.ENEMY.value)
        health = properties.get('health', 6)
        self.p1 = position
        xoffset = properties.get('xoffset', 0)
        yoffset = properties.get('yoffset', 0)
        self.p2 = position + pygame.Vector2(xoffset, yoffset)
        self.t = 0
        distance_to_move = (self.p2 - self.p1).magnitude()
        if distance_to_move > utils.EPSILON:
            self.dt = 1 / distance_to_move
        else:
            self.dt = 0
        self.shape.filter = pymunk.ShapeFilter(categories=collision.Layer.ENEMY.value, mask=collision.Layer.BLOCK.value | collision.Layer.PLATFORM.value)
        self.hp = health
        self.max_health = health
        self.color = (250, 40, 60)

    def update(self):
        self.t += self.dt
        if self.t > 1:
            self.dt = -self.dt
            self.t = 1
        if self.t < 0:
            self.dt = -self.dt
            self.t = 0
        # lerp is linear interpolation
        self.body.position = tuple(self.p1.lerp(self.p2, self.t))

    def deal_damage(self, damage):
        self.hp -= damage
        if self.hp == 0:
            self.scene.remove_object(self)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))


class EnemyFlower(Enemy):
    def __init__(self, position, properties):
        super().__init__(position, properties)
        self.color = (250, 40, 60)
        self.fire_rate = 60
        self.bullet_timer = 10

    def update(self):
        super().update()
        self.bullet_timer += 1
        self.player = self.scene.find_player()
        if self.direct_sight(self.player) and self.bullet_timer > self.fire_rate:
            self.bullet_timer = 0
            self.shoot(self.player)

    def direct_sight(self, player):
        player_pos = player.body.position
        enemy_pos = self.body.position
        if player_pos.get_distance(enemy_pos) < 2000:
            query = self.scene.physics_space.segment_query_first([
                self.body.position.x, self.body.position.y], [player_pos.x, player_pos.y], 1,
                pymunk.ShapeFilter(mask=collision.Layer.BLOCK.value | collision.Layer.PLATFORM.value))
            if query:
                if query.shape.collision_type == collision.Layer.PLAYER.value:
                    return True
        return False

    def shoot(self, player):
        start = self.body.position
        stop = player.body.position
        direction = pygame.Vector2(stop) - pygame.Vector2(start)
        self.scene.add_object(EnemyBullet(start.x, start.y, direction, speed=1.2))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))

class Spike(Solid):
    def __init__(self, position, properties=None):
        super().__init__(position.x, position.y, 50, 50,
                         body_type=pymunk.Body.STATIC, layer=collision.Layer.SPIKE.value)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))

class SpikeTile(SolidTile):
    def __init__(self, position, image, colliders):
        super().__init__(
            position, image, colliders,
            layer=collision.Layer.SPIKE.value
        )
