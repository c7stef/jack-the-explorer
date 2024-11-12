import pygame
import collision
from gameobject import GameObject
import pymunk
from rigidbody import RigidBody
from bullet import Bullet
from deathScreen import DeathScreen
import utils

# Player class
class Player(GameObject, RigidBody):
    def __init__(self, x, y):
        self.JUMP_STRENGTH = -15
        self.FIRST_IMPULSE_FACTOR = 15
        self.MOVE_STRENGTH = 150
        self.MAX_VELOCITY = 30
        self.FIRE_RATE = 15
        self.JUMP_IMPULSES_MAX = 12
        self.currentAmmo = 10
        self.maxAmmo = 100
        self.bulletHistory = 0
        self.layer = collision.Layer.PLAYER
        self.keys_pressed = set()
        self.facing = utils.Direction.RIGHT
        self.bullet_direction = {self.facing}
        self.jump_time = 0
        self.jump_impulses_left = 0

        self.moment = pymunk.moment_for_box(mass=10, size=(50, 50))
        self.body = pymunk.Body(mass=10, moment=float("inf"))
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, size=(50, 50))
        self.shape.friction = 0
        self.shape.collision_type = collision.Layer.PLAYER.value

        self.width = 50
        self.height = 50

        self.is_on_ground = False
        self.on_platform = None

        self.color = (0, 0, 255)

    def body_data(self):
        return (self.body, self.shape)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        left_pressed = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right_pressed = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        up_pressed = keys[pygame.K_w] or keys[pygame.K_UP]
        down_pressed = keys[pygame.K_s] or keys[pygame.K_DOWN]

        if left_pressed:
            self.body.apply_impulse_at_local_point((-self.MOVE_STRENGTH, 0))
            self.facing = utils.Direction.LEFT
        elif right_pressed:
            self.body.apply_impulse_at_local_point((self.MOVE_STRENGTH, 0))
            self.facing = utils.Direction.RIGHT

        if up_pressed and self.jump_impulses_left > 0:
            if self.jump_impulses_left == self.JUMP_IMPULSES_MAX:
                impulse_strength = self.JUMP_STRENGTH * self.FIRST_IMPULSE_FACTOR
            else:
                impulse_strength = self.JUMP_STRENGTH

            self.jump_impulses_left -= 1
            self.body.apply_impulse_at_local_point((0, impulse_strength))

        if not up_pressed:
            self.jump_impulses_left = 0

        if pygame.mouse.get_pressed()[0] and self.bulletHistory >= self.FIRE_RATE and self.currentAmmo > 0:
            mouse_pos = pygame.mouse.get_pos()
            relativeBodyPos = self.scene.relative_position(self.body.position)
            relativeBulletDirection = mouse_pos - relativeBodyPos
            self.currentAmmo -= 1

            self.scene.add_object(Bullet(self.body.position.x, self.body.position.y, relativeBulletDirection))
            self.bulletHistory = 0

    def update(self):
        self.bulletHistory += 1

        self.body.velocity = 0, self.body.velocity.y

        collisions = self.get_collisions()
        self.is_on_ground = False
        self.on_platform = None
        for collision_data in collisions:
            if collision_data["normal"].y < 0:
                self.is_on_ground = True
                self.jump_impulses_left = self.JUMP_IMPULSES_MAX
                if collision_data["shape"].collision_type == collision.Layer.BLOCK.value:
                    pass
                if collision_data["shape"].collision_type == collision.Layer.PLATFORM.value:
                    self.on_platform = collision_data["shape"]
                if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                    self.scene.find_rigid_body(collision_data["shape"]).color = (50, 50, 50)
                    self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                    self.body.apply_impulse_at_local_point((0, self.JUMP_STRENGTH * self.FIRST_IMPULSE_FACTOR))
            if collision_data["normal"].x != 0:
                if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                    self.color = (200, 0, 100)
                    self.scene.remove_object(self)
                    self.scene.add_object(DeathScreen(self.scene))

            if collision_data["shape"].collision_type == collision.Layer.COIN.value:
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))

            if collision_data["shape"].collision_type == collision.Layer.AMMOBOX.value:
                self.currentAmmo += self.scene.find_rigid_body(collision_data["shape"]).ammoAmount
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                if self.currentAmmo > self.maxAmmo:
                    self.currentAmmo = self.maxAmmo

            if collision_data["shape"].collision_type == collision.Layer.DECBLOCK.value:
                self.scene.find_rigid_body(collision_data["shape"]).decay()


        self.handle_input()

        if self.body.velocity.y < -self.MAX_VELOCITY:
            self.body.velocity = self.body.velocity.x, -self.MAX_VELOCITY

        if self.on_platform:
            platform_velocity = self.on_platform.body.velocity
            self.body.apply_impulse_at_local_point(platform_velocity * 10)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))

