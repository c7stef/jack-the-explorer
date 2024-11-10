from solid import Solid
import pygame
import pymunk
import collision

class MovingPlatform(Solid):
    def __init__(self, width, height, p1, p2):
        super().__init__(p1.x, p1.y, width, height, pymunk.Body.KINEMATIC)
        self.shape.friction = 0.5
        self.p1 = p1
        self.p2 = p2
        self.t = 0
        self.dt = 0.01
        self.shape.collision_type = collision.Layer.PLATFORM.value
        
    def update(self):
        self.t += self.dt
        if self.t > 1:
            self.dt = -self.dt
            self.t = 1
        if self.t < 0:
            self.dt = -self.dt
            self.t = 0
        # lerp is linear interpolation
        # self.body.position = tuple(self.p1.lerp(self.p2, self.t))
        self.body.velocity = (3, 2)

    def draw(self, screen):
        pygame.draw.rect(screen, (60, 200, 200), self.scene.relative_rect(pygame.Rect(self.body.position.x - self.rect.w / 2, self.body.position.y - self.rect.h / 2, self.rect.width, self.rect.height)))