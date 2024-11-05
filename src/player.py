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
        self.gravityApply = True

    def printPosition(self):
        print("Player data:")
        print(self.position)
        print(self.rect)
        print("Right px: " + str(self.rect.right))

    def set_position_x(self, x):
        self.position.x = x
        self.rect.x = x

    def set_position_y(self, y):
        self.position.y = y
        self.rect.y = y

    def set_position(self, x, y):
        self.set_position_x(x)
        self.set_position_y(y)

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
        if self.gravityApply:
            self.velocity.y += self.gravity

    def posMainDiag(self, x1, x2, y1, y2, offset):
        xA, yA = self.rect.center
        yA += self.rect.height / offset
        v1 = (x2-x1, y2-y1)   # Vector 1
        v2 = (x2-xA, y2-yA)   # Vector 2
        xp = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product (magnitude)
        if xp > 0:
            # Over main diag
            return True
        else:
            # Under main diag
            return False

    def posSecDiag(self, x1, x2, y1, y2, offset):
        xA, yA = self.rect.center
        yA += self.rect.height / offset
        v1 = (x2-x1, y2-y1)   # Vector 1
        v2 = (x2-xA, y2-yA)   # Vector 2
        xp = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product (magnitude)
        if xp > 0:
            # Under sec diag
            return False
        else:
            # Over main diag
            return True

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.set_position_x(self.position.x + self.velocity.x)
        self.set_position_y(self.position.y + self.velocity.y)
        self.gravityApply = True

        collisions = self.scene.get_collisions(self)
        for other in collisions:
            if isinstance(other, Block):
                x1, y1 = other.rect.topleft
                x2, y2 = other.rect.bottomright
                isAboveMain = self.posMainDiag(x1, x2, y1, y2, 4)
                x1, y1 = other.rect.topright
                x2, y2 = other.rect.bottomleft
                isAboveSec = self.posSecDiag(x1, x2, y1, y2, 4)
                # Case 1: when a rectangle (rect) falls onto a block, the rectangle doesn't know
                # that it needs to fall onto the block. If the bottom of the rectangle reaches or
                # exceeds the top of the block, then I will raise it such that we know it is resting on the block
                if isAboveMain and isAboveSec:
                    self.gravityApply = False
                    self.set_position_y(other.rect.top - self.rect.height)
                    self.velocity.y = 0
                    self.is_jumping = False
                    print("player is on block")
                    continue
                # Case 2.1 Left of the block
                elif not isAboveMain and isAboveSec:
                    self.set_position_x(other.rect.left - self.rect.width)
                    self.velocity.x = 0
                    print("Left of block")
                    continue
                # Case 3.1 Right of the block
                elif isAboveMain and not isAboveSec:
                    self.set_position_x(other.rect.right)
                    self.velocity.x = 0
                    print("Right of block")
                    continue
                # Case 4 under the block
                elif not isAboveMain and not isAboveSec:
                    if abs(other.rect.bottom - self.rect.top) < 10:
                        self.set_position_y(other.rect.bottom)
                        self.velocity.y = 0
                    else:
                        self.velocity.x = 0
                        # Case 2.2
                        if abs(self.rect.right - other.rect.left) < \
                        abs(self.rect.left - other.rect.right):
                            self.set_position_x(other.rect.left - self.rect.width)
                        # Case 3.2
                        else:
                            self.set_position_x(other.rect.right)

    def draw(self, screen):
        # self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 255), self.rect)

