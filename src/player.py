import pygame
import pymunk
import math

from display_data import DeathScreen, DisplayData, PauseScreen, FinishScreen
from gameobject import GameObject, RigidBody, Followable

from animated_sprite import AnimatedSprite
from image_processing import scale_surface_contain

import collision
import utils

coin_sound = pygame.mixer.Sound("sounds/coin.wav")
ammo_sound = pygame.mixer.Sound("sounds/ammo_found.mp3")
health_sound = pygame.mixer.Sound("sounds/health.mp3")
damage_taken_sound = pygame.mixer.Sound("sounds/hurt.mp3")

# Player class
class Player(GameObject, RigidBody, Followable):
    def __init__(self, x, y, level):
        self.level = level
        self.lives = 3
        self.hp_per_life = 3
        self.current_hp = self.hp_per_life
        self.respawn_position = pygame.Vector2(x, y)
        self.JUMP_STRENGTH = -2.85
        self.FIRST_IMPULSE_FACTOR = 10
        self.MOVE_STRENGTH = 4.5
        self.MAX_VELOCITY = 300
        self.FIRE_RATE = 15
        self.JUMP_IMPULSES_MAX = 15
        self.HORIZONTAL_DRAG = 17/20
        self.VERTICAL_NORMAL_Y = 0.3
        self.HORIZONTAL_NORMAL_X = math.sqrt(1 - self.VERTICAL_NORMAL_Y ** 2)

        self.jump_time = 0
        self.jump_impulses_left = 0
        self.level.score = 0
        self.level.coin_cnt = 0
        self.scene = level.scene
        self.display = DisplayData(self)
        self.scene.add_object(self.display)

        self.moment = pymunk.moment_for_box(mass=1, size=(62, 62))
        self.body = pymunk.Body(mass=1, moment=float("inf"))
        self.body.position = (x, y)

        self.shape = pymunk.Poly.create_box(self.body, size=(10, 10), radius=20)
        self.shape.friction = 0
        self.shape.collision_type = collision.Layer.PLAYER.value

        self.width = 62
        self.height = 62

        self.is_on_ground = False
        self.on_platform = None
        self.jump_held = False
        self.transportable = False
        self.color = (0, 0, 255)

        self.orientation = 1
        self.running = False

        self.last_checkpoint = None

        self.idle_sprite = AnimatedSprite("assets/player/idle", (62, 62), 16)
        self.idle_sprite_flipped = self.idle_sprite.flipped()

        self.running_sprite = AnimatedSprite("assets/player/running", (62, 62), 3)
        self.running_sprite_flipped = self.running_sprite.flipped()

        self.jump_sprite = scale_surface_contain(pygame.image.load("assets/player/jump/jump_up.png"), (62, 62))
        self.jump_sprite_flipped = pygame.transform.flip(self.jump_sprite, True, False)

        self.fall_sprite = scale_surface_contain(pygame.image.load("assets/player/jump/jump_fall.png"), (62, 62))
        self.fall_sprite_flipped = pygame.transform.flip(self.fall_sprite, True, False)

        self.hit_sprite = scale_surface_contain(pygame.image.load("assets/player/hit/frame-got-hit.png"), (62, 62))
        self.hit_sprite_flipped = pygame.transform.flip(self.hit_sprite, True, False)

        self.current_sprite = self.idle_sprite

    @property
    def position(self):
        return pygame.Vector2(self.body.position.x, self.body.position.y)

    def body_data(self):
        return (self.body, self.shape)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        left_pressed = keys[utils.controls['left']]
        right_pressed = keys[utils.controls['right']]
        up_pressed = keys[utils.controls['up']]
        down_pressed = keys[utils.controls['down']]

        if down_pressed and self.transportable:
            self.transport_player(self.tunnel)

        if keys[pygame.K_ESCAPE] and not utils.escape_pressed:
            utils.current_screen = PauseScreen(self.level)
            utils.escape_pressed = True
        if not keys[pygame.K_ESCAPE]:
            utils.escape_pressed = False

        if left_pressed:
            self.body.apply_impulse_at_local_point((-self.MOVE_STRENGTH, 0))
            self.orientation = -1
            self.running = True
        elif right_pressed:
            self.body.apply_impulse_at_local_point((self.MOVE_STRENGTH, 0))
            self.orientation = 1
            self.running = True
        else:
            self.running = False

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

        if keys[utils.controls['reload']]:
            self.weapon.reload()

        if pygame.mouse.get_pressed()[0]:
            self.weapon.fire()

    def transport_player(self, tunnel_in):
        if tunnel_in.linked_tunnel:
            self.body.position = tunnel_in.linked_tunnel.hole_position
            self.body.velocity = (0, 0)

    def update(self):
        self.body.velocity = self.body.velocity.x*self.HORIZONTAL_DRAG, self.body.velocity.y
        self.transportable = False
        collisions = self.get_collisions()
        self.is_on_ground = False
        self.on_platform = None
        for collision_data in collisions:
            if collision_data["shape"].collision_type == collision.Layer.SPIKE.value:
                self.die()

            # Normal is mostly upwards
            if collision_data["normal"].y < -self.VERTICAL_NORMAL_Y:
                # Player is on the ground and can jump again
                if collision_data["shape"].collision_type in {
                    collision.Layer.BLOCK.value,
                    collision.Layer.PLATFORM.value,
                    collision.Layer.TUNNEL.value,
                    collision.Layer.DECBLOCK.value
                }:
                    self.is_on_ground = True
                    if not self.jump_held:
                        self.jump_impulses_left = self.JUMP_IMPULSES_MAX

                # Player is on moving platform
                if collision_data["shape"].collision_type == collision.Layer.PLATFORM.value:
                    self.on_platform = collision_data["shape"]

                # Player stepped on enemy
                if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                    self.scene.find_rigid_body(collision_data["shape"]).color = (50, 50, 50)
                    self.body.apply_impulse_at_local_point((0, self.JUMP_STRENGTH * self.FIRST_IMPULSE_FACTOR))
                    self.level.score += 100 * self.scene.find_rigid_body(collision_data["shape"]).max_health
                    enemy = self.scene.find_rigid_body(collision_data["shape"])
                    enemy.deal_damage(enemy.hp)

                # Player is on tunnel
                if collision_data["shape"].collision_type == collision.Layer.TUNNEL.value:
                    self.transportable = True
                    self.tunnel = self.scene.find_rigid_body(collision_data["shape"])

                # Player is on a decaying block
                if collision_data["shape"].collision_type == collision.Layer.DECBLOCK.value:
                    self.scene.find_rigid_body(collision_data["shape"]).decay()

            # Collision is to the side
            if abs(collision_data["normal"].x) > self.HORIZONTAL_NORMAL_X:
                if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                    self.die()

            # Player collides with a coin
            if collision_data["shape"].collision_type == collision.Layer.COIN.value:
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                self.level.coin_cnt += 1
                self.level.score += 10
                coin_sound.play()
                coin_sound.set_volume(utils.controls['sound'])

            # Player collides with an ammo box
            if collision_data["shape"].collision_type == collision.Layer.AMMOBOX.value:
                self.weapon.pick_up_ammo(self.scene.find_rigid_body(collision_data["shape"]).ammo_amount)
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                self.level.score += 10
                ammo_sound.play()
                ammo_sound.set_volume(utils.controls['sound'])

            # Player collides with a health box
            if collision_data["shape"].collision_type == collision.Layer.HEALTHBOX.value:
                self.current_hp = min(3, self.current_hp + 1)
                self.scene.remove_object(self.scene.find_rigid_body(collision_data["shape"]))
                self.level.score += 10
                health_sound.play()
                health_sound.set_volume(utils.controls['sound'])

            if collision_data["shape"].collision_type == collision.Layer.CHECKPOINT.value:
                self.last_checkpoint = self.scene.find_rigid_body(collision_data["shape"]).reached(self)

        self.handle_input()

        if self.body.velocity.y < -self.MAX_VELOCITY:
            self.body.velocity = self.body.velocity.x, -self.MAX_VELOCITY

        if self.on_platform:
            platform_velocity = self.on_platform.body.velocity
            self.body.apply_impulse_at_local_point(platform_velocity * 0.15)

        if self.out_of_bounds():
            self.die()

        if self.reached_end():
            utils.current_screen = FinishScreen(self.level)
        
        if isinstance(self.current_sprite, AnimatedSprite):
            self.current_sprite.update()
        
        if self.is_on_ground:
            if self.running:
                self.current_sprite = self.running_sprite if self.orientation == 1 else self.running_sprite_flipped
            else:
                self.current_sprite = self.idle_sprite if self.orientation == 1 else self.idle_sprite_flipped
        else:
            if self.body.velocity.y < 0:
                self.current_sprite = self.jump_sprite if self.orientation == 1 else self.jump_sprite_flipped
            else:
                self.current_sprite = self.fall_sprite if self.orientation == 1 else self.fall_sprite_flipped

    def deal_damage(self, damage):
        damage_taken_sound.play()
        damage_taken_sound.set_volume(utils.controls['sound'])
        self.current_hp -= damage

        if self.current_hp <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.respawn()
                self.current_hp = self.hp_per_life
            else:
                self.die()

    def respawn(self):
        self.body.position = self.respawn_position.x, self.respawn_position.y
        if self.last_checkpoint:
            self.body.position = self.last_checkpoint.body.position
        self.body.velocity = (0, 0)

    def equip_weapon(self, weapon):
        self.weapon = weapon

    def out_of_bounds(self):
        if self.body.position.y + self.height / 2 > self.scene.map_bounds.bottom:
            return True
        return False

    def reached_end(self):
        if self.body.position.x + self.width / 2 > self.scene.map_bounds.right:
            return True
        return False

    def die(self):
        last_checkpoint = self.last_checkpoint

        self.scene.remove_object(self.display)
        self.scene.remove_object(self)

        utils.current_screen = DeathScreen(self.level, last_checkpoint)

    def draw(self, screen):
        if isinstance(self.current_sprite, AnimatedSprite):
            self.current_sprite.draw(screen, self.scene.relative_position(self.body.position))
        else:
            screen.blit(self.current_sprite, self.scene.relative_position(self.body.position - pygame.Vector2(self.current_sprite.get_size()) / 2))
