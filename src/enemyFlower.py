from enemy import Enemy
import collision
import pygame
from enemyBullet import EnemyBullet
import utils
import pymunk

class EnemyFlower(Enemy):
    def __init__(self, p1, p2, health):
        super().__init__(p1, p2, health)
        self.color = (250, 40, 60)
        self.fireRate = 10
        self.bulletTimer = 10

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
        if self.directSight(utils.player) and self.bulletTimer > self.fireRate:
            self.bulletTimer = 0
            self.shoot(utils.player)

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