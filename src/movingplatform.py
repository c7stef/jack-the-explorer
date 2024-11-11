from solid import Solid
import pygame
import pymunk
import collision
import math
import utils

class MovingPlatform(Solid):
    def __init__(self, width, height, p1, p2, speed):
        super().__init__(p1.x, p1.y, width, height, pymunk.Body.KINEMATIC)
        self.shape.friction = 0.5
        self.p1 = p1
        self.p2 = p2
        self.forward = True
        self.speed_vector = pygame.Vector2.normalize(p2 - p1) * speed
        self.shape.collision_type = collision.Layer.PLATFORM.value
        
    def update(self):
        if math.fabs(self.p1.x - self.p2.x) < utils.EPSILON:
            t = (self.body.position.y - self.p1.y) / (self.p2.y - self.p1.y)
        else:
            t = (self.body.position.x - self.p1.x) / (self.p2.x - self.p1.x)

        if t > 1:
            self.forward = False
        if t < 0:
            self.forward = True
        
        final_velocity = self.speed_vector if self.forward else -self.speed_vector
        self.body.velocity = (final_velocity.x, final_velocity.y)

    def draw(self, screen):
        pygame.draw.rect(screen, (60, 200, 200), self.scene.relative_rect(pygame.Rect(self.body.position.x - self.rect.w / 2, self.body.position.y - self.rect.h / 2, self.rect.width, self.rect.height)))