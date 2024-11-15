from block import Solid
from bullet import EnemyBullet
import pygame
import pymunk
import collision

class Enemy(Solid):
    def __init__(self, p1, p2, health):
        self.width = 50
        self.height = 50
        super().__init__(p1.x, p1.y, self.width, self.height, pymunk.Body.KINEMATIC)
        self.shape.friction = 0.5
        self.p1 = p1
        self.p2 = p2
        self.t = 0
        self.dt = 0.01
        self.shape.collision_type = collision.Layer.ENEMY.value
        self.shape.filter = pymunk.ShapeFilter(categories=collision.Layer.ENEMY.value, mask=collision.Layer.BLOCK.value | collision.Layer.PLATFORM.value)
        self.hp = health
        self.maxHealth = health
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
    def __init__(self, p1, p2, health, level):
        super().__init__(p1, p2, health)
        self.color = (250, 40, 60)
        self.fireRate = 10
        self.bulletTimer = 10
        self.level = level

    def update(self):
        self.t += self.dt
        if self.t > 1:
            self.dt = -self.dt
            self.t = 1
        if self.t < 0:
            self.dt = -self.dt
            self.t = 0
        self.bulletTimer += 1
        self.body.position = tuple(self.p1.lerp(self.p2, self.t))
        if self.directSight(self.level.player) and self.bulletTimer > self.fireRate:
            self.bulletTimer = 0
            self.shoot(self.level.player)

    def directSight(self, player):
        playerPos = player.body.position
        enemyPos = self.body.position
        if playerPos.get_distance(enemyPos) < 2000:
            query = self.scene.physics_space.segment_query_first([
                self.body.position.x, self.body.position.y], [playerPos.x, playerPos.y], 1,
                pymunk.ShapeFilter(mask=collision.Layer.BLOCK.value | collision.Layer.PLATFORM.value))
            if query:
                if query.shape.collision_type == collision.Layer.PLAYER.value:
                    return True
        return False



    def shoot(self, player):
        start = self.body.position
        stop = player.body.position
        dir = pygame.Vector2(stop) - pygame.Vector2(start)
        self.scene.add_object(EnemyBullet(start.x, start.y, dir))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))