import pygame
import pymunk

from displayData import DeathScreen, DisplayData, PauseScreen
from gameobject import GameObject, RigidBody, Followable
from bullet import Bullet

from gun import Weapon

import collision
import utils

# Player class
class Player(GameObject, RigidBody, Followable):
    def __init__(self, x, y, level):
        self.level = level

        self.JUMP_STRENGTH = -2.85
        self.FIRST_IMPULSE_FACTOR = 10
        self.MOVE_STRENGTH = 4.5
        self.MAX_VELOCITY = 300
        self.FIRE_RATE = 15
        self.JUMP_IMPULSES_MAX = 15
        
        self.jump_time = 0
        self.jump_impulses_left = 0
        self.level.score = 0
        self.level.coinCnt = 0
        self.scene = level.scene
        self.display = DisplayData(self)
        self.scene.add_object(self.display)

        self.moment = pymunk.moment_for_box(mass=1, size=(50, 50))
        self.body = pymunk.Body(mass=1, moment=float("inf"))
        self.body.position = (x, y)

        self.shape = pymunk.Poly.create_box(self.body, size=(10, 10), radius=20)
        self.shape.friction = 0
        self.shape.collision_type = collision.Layer.PLAYER.value

        self.width = 50
        self.height = 50

        self.is_on_ground = False
        self.on_platform = None
        self.jump_held = False
        self.transportable = False
        self.color = (0, 0, 255)

    @property
    def position(self):
        return pygame.Vector2(self.body.position.x, self.body.position.y)

    def body_data(self):
        return (self.body, self.shape)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        left_pressed = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right_pressed = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        up_pressed = keys[pygame.K_w] or keys[pygame.K_UP]
        down_pressed = keys[pygame.K_s] or keys[pygame.K_DOWN]

        if down_pressed and self.transportable:
            self.transport_player(self.tunnel)

        if keys[pygame.K_ESCAPE] and not utils.escapePressed:
            utils.currentScreen = PauseScreen(self.level)
            utils.escapePressed = True
        if not keys[pygame.K_ESCAPE]:
            utils.escapePressed = False

        if left_pressed:
            self.body.apply_impulse_at_local_point((-self.MOVE_STRENGTH, 0))
        elif right_pressed:
            self.body.apply_impulse_at_local_point((self.MOVE_STRENGTH, 0))

        if up_pressed and self.jump_impulses_left > 0:
            if self.jump_impulses_left == self.JUMP_IMPULSES_MAX:
                impulse_strength = self.JUMP_STRENGTH * self.FIRST_IMPULSE_FACTOR
            else:
                impulse_strength = self.JUMP_STRENGTH * self.jump_impulses_left / self.JUMP_IMPULSES_MAX

            self.jump_impulses_left -= 1
            self.body.apply_impulse_at_local_point((0, impulse_strength))
            self.jump_held = True


        if not up_pressed:
            self.jump_impulses_left = 0
            self.jump_held = False

        if keys[pygame.K_r]:
            self.weapon.reload()

        if pygame.mouse.get_pressed()[0]:
            self.weapon.fire()

    def transport_player(self, tunnel_in):
        if tunnel_in.linked_tunnel and not tunnel_in.linked_tunnel.upwards:
            self.body.position = tunnel_in.linked_tunnel.body.position.x, tunnel_in.linked_tunnel.body.position.y + tunnel_in.linked_tunnel.height
            self.body.velocity = (0, 0)

        if tunnel_in.linked_tunnel and tunnel_in.linked_tunnel.upwards:
                self.body.position = tunnel_in.linked_tunnel.body.position.x, tunnel_in.linked_tunnel.body.position.y - tunnel_in.linked_tunnel.height
                self.body.velocity = (0, 0)

    def update(self):

        self.body.velocity = self.body.velocity.x*17/20, self.body.velocity.y
        self.transportable = False
        collisions = self.get_collisions()
        self.is_on_ground = False
        self.on_platform = None
        for collision_data in collisions:
            if collision_data["shape"].collision_type == collision.Layer.SPIKE.value:
                    self.color = (200, 0, 100)
                    self.scene.remove_object(self.display)
                    self.scene.remove_object(self)
                    utils.currentScreen = DeathScreen(self.level)
            
            if collision_data["normal"].y < -0.4:
                self.is_on_ground = True
                if not self.jump_held:
                    self.jump_impulses_left = self.JUMP_IMPULSES_MAX
                if collision_data["shape"].collision_type == collision.Layer.BLOCK.value:
                    pass
                if collision_data["shape"].collision_type == collision.Layer.PLATFORM.value:
                    self.on_platform = collision_data["shape"]
                if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                    self.scene.find_rigid_body(collision_data["shape"]).color = (50, 50, 50)
                    self.body.apply_impulse_at_local_point((0, self.JUMP_STRENGTH * self.FIRST_IMPULSE_FACTOR))
                    self.level.score += 100 * self.scene.find_rigid_body(collision_data["shape"]).maxHealth
                    self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                if collision_data["shape"].collision_type == collision.Layer.TUNNEL.value:
                    self.transportable = True
                    self.tunnel = self.scene.find_rigid_body(collision_data["shape"])
                    #self.transport_player(self.scene.find_rigid_body(collision_data["shape"]))

            if collision_data["normal"].x != 0:
                if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                    self.color = (200, 0, 100)
                    self.scene.remove_object(self.display)
                    self.scene.remove_object(self)
                    utils.currentScreen = DeathScreen(self.level)

            if collision_data["shape"].collision_type == collision.Layer.COIN.value:
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                self.level.coinCnt += 1
                self.level.score += 10

            if collision_data["shape"].collision_type == collision.Layer.AMMOBOX.value:
                self.weapon.pickUpAmmo(self.scene.find_rigid_body(collision_data["shape"]).ammoAmount)
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                self.level.score += 10

            if collision_data["shape"].collision_type == collision.Layer.HEALTHBOX.value:
                self.level.hp += self.scene.find_rigid_body(collision_data["shape"]).healthAmount
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                if self.level.hp > self.level.maxHp:
                    self.level.hp = self.level.maxHp
                self.level.score += 10

            
               

            if collision_data["shape"].collision_type == collision.Layer.DECBLOCK.value:
                self.scene.find_rigid_body(collision_data["shape"]).decay()

        self.handle_input()

        if self.body.velocity.y < -self.MAX_VELOCITY:
            self.body.velocity = self.body.velocity.x, -self.MAX_VELOCITY

        if self.on_platform:
            platform_velocity = self.on_platform.body.velocity
            self.body.apply_impulse_at_local_point(platform_velocity * 0.15)

    def deal_damage(self, damage):
        self.level.hp -= damage
        if self.level.hp <= 0:
            self.scene.remove_object(self.display)
            self.scene.remove_object(self)
            utils.currentScreen = DeathScreen(self.level)

    def equipWeapon(self, weapon):
        self.weapon = weapon

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.scene.relative_rect(pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height)))

