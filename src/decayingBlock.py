from solid import Solid
import pygame
import pymunk
import collision

class DecayingBlock(Solid):
    def __init__(self, x, y, width, height, ttl):
        super().__init__(x, y, width, height, pymunk.Body.STATIC)
        self.shape.collision_type = collision.Layer.DECBLOCK.value
        self.color = (139, 69, 19)
        self.ttl = ttl

    def update(self):
        if self.ttl < 0:
            self.scene.remove_object(self)

    def decay(self):
        self.ttl -= 1
        self.color = (
            max(self.color[0] - 1, 0),
            max(self.color[1] - 1, 0),
            max(self.color[2] - 1, 0)
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.scene.relative_rect(pygame.Rect(self.body.position.x - self.rect.w / 2, self.body.position.y - self.rect.h / 2, self.rect.width, self.rect.height)))
