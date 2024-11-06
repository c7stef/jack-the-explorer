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

    def posAboveHalf(self, other):
        if other.rect.y + other.rect.height / 2 < self.rect.y + self.rect.height / 2:
            return False
        return True

    def posAboveFirst(self, other):
        xA, yA = self.rect.center
        x1, y1 = other.rect.topleft
        x2 = other.rect.x + other.rect.height / 2
        y2 = other.rect.y + other.rect.height / 2
        v1 = (x2-x1, y2-y1)
        v2 = (x2-xA, y2-yA)
        xp = v1[0]*v2[1] - v1[1]*v2[0]
        if xp > 0:
            return True
        return False

    def posAboveSecond(self, other):
        xA, yA = self.rect.center
        x1, y1 = other.rect.topright
        x2 = other.rect.right - other.rect.height / 2
        y2 = other.rect.y + other.rect.height / 2
        v1 = (x2-x1, y2-y1)
        v2 = (x2-xA, y2-yA)
        xp = v1[0]*v2[1] - v1[1]*v2[0]
        if xp > 0:
            return False
        return True

    # Freestyle
    def posAboveThird(self, other):
        xA, yA = self.rect.center
        x1, y1 = other.rect.bottomright
        x2 = other.rect.right - other.rect.height / 2
        y2 = other.rect.bottom - other.rect.height / 2
        v1 = (x2-x1, y2-y1)
        v2 = (x2-xA, y2-yA)
        xp = v1[0]*v2[1] - v1[1]*v2[0]
        if xp > 0:
            return False
        return True

    def posAboveFourth(self, other):
        xA, yA = self.rect.center
        x1, y1 = other.rect.bottomleft
        x2 = other.rect.x + other.rect.height / 2
        y2 = other.rect.bottom - other.rect.height / 2
        v1 = (x2-x1, y2-y1)
        v2 = (x2-xA, y2-yA)
        xp = v1[0]*v2[1] - v1[1]*v2[0]
        if xp > 0:
            return True
        return False

    def handleUnderBlock(self, other):
        self.set_position_y(other.rect.bottom)
        self.velocity.y = 0
        print("Under block")

    def handleLeftBlock(self, other):
        self.set_position_x(other.rect.left - self.rect.width)
        self.velocity.x = 0
        print("Left of block")

    def handleRightBlock(self, other):
        self.set_position_x(other.rect.right)
        self.velocity.x = 0
        print("Right of block")

    def handleOnBlock(self, other):
        self.gravityApply = False
        self.set_position_y(other.rect.top - self.rect.height)
        self.velocity.y = 0
        self.is_jumping = False
        print("player is on block")

    def getPos(self, other):
        self.isAboveHalf = self.posAboveHalf(other)
        self.isAboveFirst = self.posAboveFirst(other)
        self.isAboveSec = self.posAboveSecond(other)
        self.isAboveThird = self.posAboveThird(other)
        self.isAboveFourth = self.posAboveFourth(other)

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.set_position_x(self.position.x + self.velocity.x)
        self.set_position_y(self.position.y + self.velocity.y)
        self.gravityApply = True

        collisions = self.scene.get_collisions(self)
        for other in collisions:
            if isinstance(other, Block):
                self.getPos(other)
                if self.isAboveHalf:
                    if self.isAboveFirst and self.isAboveSec:
                        self.handleOnBlock(other)
                    elif self.isAboveFirst and not self.isAboveSec:
                        self.handleRightBlock(other)
                    elif not self.isAboveFirst and self.isAboveSec:
                        self.handleLeftBlock(other)
                elif not self.isAboveHalf:
                    if self.isAboveThird and not self.isAboveFourth:
                        self.handleRightBlock(other)
                    elif not self.isAboveThird and self.isAboveFourth:
                        self.handleLeftBlock(other)
                    elif not self.isAboveThird and not self.isAboveFourth:
                        self.handleUnderBlock(other)

    def draw(self, screen):
        # self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 255), self.rect)

