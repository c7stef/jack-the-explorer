import pygame
import collision
from gameobject import GameObject
import pymunk
from rigidbody import RigidBody
from bullet import Bullet, Direction

# Player class
class Player(GameObject, RigidBody):
    def __init__(self, x, y):
        self.JUMP_STRENGTH = -300
        self.MOVE_STRENGTH = 150
        self.MAX_VELOCITY = 30
        self.FIRE_RATE = 15
        self.bulletHistory = 0
        self.layer = collision.Layer.PLAYER

        self.moment = pymunk.moment_for_box(mass=10, size=(50, 50))
        self.body = pymunk.Body(mass=10, moment=float("inf"))
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, size=(50, 50))
        self.shape.friction = 0
        self.shape.collision_type = collision.Layer.PLAYER.value
        self.shape.filter = pymunk.ShapeFilter(group=collision.COLLISION_DISABLED)

        self.width = 50
        self.height = 50

        self.is_on_ground = False
        self.on_platform = None

        self.color = (0, 0, 255)

    def body_data(self):
        return (self.body, self.shape)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.body.apply_impulse_at_local_point((-self.MOVE_STRENGTH, 0))
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.body.apply_impulse_at_local_point((self.MOVE_STRENGTH, 0))

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.is_on_ground:
            self.body.apply_impulse_at_local_point((0, self.JUMP_STRENGTH))

        if keys[pygame.K_SPACE] and self.bulletHistory >= self.FIRE_RATE:
            self.scene.add_object(Bullet(self.body.position.x, self.body.position.y, {Direction.RIGHT}))
            self.bulletHistory = 0

    def update(self):
        self.bulletHistory += 1

        self.body.velocity = 0, self.body.velocity.y

        collisions = self.get_collisions()
        # print(collisions)
        self.is_on_ground = False
        self.on_platform = None
        for collision_data in collisions:
            if collision_data["normal"].y < 0:
                self.is_on_ground = True
                if collision_data["shape"].collision_type == collision.Layer.BLOCK.value:
                    pass
                if collision_data["shape"].collision_type == collision.Layer.PLATFORM.value:
                    self.on_platform = collision_data["shape"]
                if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                    self.scene.find_rigid_body(collision_data["shape"]).color = (50, 50, 50)
                    self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                    self.body.apply_impulse_at_local_point((0, self.JUMP_STRENGTH))
            if collision_data["normal"].x != 0:
                if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                    self.color = (200, 0, 100)
                    self.scene.remove_object(self)

            if collision_data["shape"].collision_type == collision.Layer.COIN.value:
                self.color = (40, 250, 250)
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))

        self.handle_input()

        if self.body.velocity.y < -self.MAX_VELOCITY:
            self.body.velocity = self.body.velocity.x, -self.MAX_VELOCITY

        if self.on_platform:
            relative_velocity = self.body.velocity - self.on_platform.body.velocity
            friction_force = -relative_velocity
            self.body.apply_impulse_at_local_point(friction_force * 5)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height))

