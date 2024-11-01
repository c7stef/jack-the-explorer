import pygame
import collision
from block import Block
from gameobject import GameObject

# Player class
class Player(GameObject):
    def __init__(self, x, y):
        self.layer = collision.Layer.PLAYER
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.width = 50
        self.height = 50
        self.speed = 5
        self.gravity = 0.5
        self.jump_strength = -10
        self.is_jumping = False
    
    def set_position_x(self, x):
        self.position.x = x
        self.rect.x = x

    def set_position_y(self, y):
        self.position.y = y
        self.rect.y = y

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity.y = self.jump_strength
            self.is_jumping = True

    def apply_gravity(self):
        self.velocity.y += self.gravity

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.set_position_x(self.position.x + self.velocity.x)
        self.set_position_y(self.position.y + self.velocity.y)

        collisions = self.scene.get_collisions(self)
        for other in collisions:
            if isinstance(other, Block):
                # Case 1: when a rectangle (rect) falls onto a block, the rectangle doesn't know
                # that it needs to fall onto the block. If the bottom of the rectangle reaches or
                # exceeds the top of the block, then I will raise it such that we know it is resting on the block
                if self.rect.bottom >= other.rect.top:
                    self.set_position_y(other.rect.top - self.rect.height)
                    self.velocity.y = 0
                    self.is_jumping = False

    def draw(self, screen):
        player_rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 255), player_rect)