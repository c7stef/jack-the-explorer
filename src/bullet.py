import pygame
import pymunk

from gameobject import Solid, GameObject
import collision
import utils
import math

player_bullet_sprite = pygame.image.load("assets/bullet/player_bullet.png")
enemy_bullet_sprite = pygame.image.load("assets/bullet/enemy_bullet.png")

bullet_hit_wall_sound = pygame.mixer.Sound("sounds/bullet_hit_wall.wav")
enemy_hit_sound = pygame.mixer.Sound("sounds/hit_sound.mp3")

class BulletBlast(GameObject):
    def __init__(self, x, y, color):
        self.LIFETIME = 10
        self.progress = 0
        self.position = pygame.Vector2(x, y)
        self.circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        self.color = color

    def update(self):
        self.progress += 1
        if self.progress >= self.LIFETIME:
            self.scene.remove_object(self)

    def draw(self, screen):
        self.circle_surface.fill((0, 0, 0, 0))

        pygame.draw.circle(
            self.circle_surface,
            (*self.color, 200 * (1 - self.progress / self.LIFETIME)),
            self.circle_surface.get_rect().center,
            80 * self.progress / self.LIFETIME
        )

        screen.blit(
            self.circle_surface,
            self.scene.relative_position(
                self.position - pygame.Vector2(self.circle_surface.get_rect().size) / 2
            )
        )

class Bullet(Solid):
    def __init__(self, x, y, directions, speed=1):
        super().__init__(x, y, 20, 20,
                         body_type=pymunk.Body.KINEMATIC,
                         layer=collision.Layer.BULLET.value)
        self.VELOCITY = 15
        self.shape.sensor = True
        self.position = pygame.Vector2(x, y)
        self.body.position = self.position.x, self.position.y
        self.ttl = 80
        self.direction_vector = directions.normalize() * self.VELOCITY
        self.speed = speed
        self.image_base = player_bullet_sprite

    @property
    def image(self):
        if not hasattr(self, "_image") or self._image is None:
            angle = math.degrees(math.atan2(-self.direction_vector.y, self.direction_vector.x))
            self._image = pygame.transform.rotate(self.image_base, angle)
        return self._image

    @property
    def rotated_rect(self):
        if not hasattr(self, "_rotated_rect") or self._rotated_rect is None:
            self._rotated_rect = self.image.get_rect(center=self.position)
        return self._rotated_rect

    def update(self):
        self.ttl -= 1
        if self.ttl < 0:
            self.scene.remove_object(self)
            return

        self.position += self.direction_vector * self.speed
        self.body.position = self.position.x, self.position.y

        collisions = self.get_collisions()

        set_to_die = False
        for collision_data in collisions:
            if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                self.scene.find_rigid_body(collision_data["shape"]).deal_damage(1)
                enemy_hit_sound.play()

            set_to_die = True

        if set_to_die:
            self.scene.add_object(BulletBlast(self.body.position.x, self.body.position.y, (200, 230, 255)))
            self.scene.remove_object(self)
            bullet_hit_wall_sound.play()
            bullet_hit_wall_sound.set_volume(utils.controls['sound'])

    def draw(self, screen):
        screen.blit(self.image, self.scene.relative_position(pygame.Vector2(self.body.position) - pygame.Vector2(self.rotated_rect.size) / 2))

class EnemyBullet(Bullet):
    def __init__(self, x, y, direction, speed=1):
        super().__init__(x, y, direction, speed)
        self.shape.collision_type = collision.Layer.ENEMYBULLET.value
        self.image_base = enemy_bullet_sprite

    def update(self):
        self.ttl -= 1
        if self.ttl < 0:
            self.scene.remove_object(self)
            return

        self.position += self.direction_vector * self.speed
        self.body.position = self.position.x, self.position.y

        collisions = self.get_collisions()

        set_to_die = False
        for collision_data in collisions:
            if collision_data["shape"].collision_type == collision.Layer.PLAYER.value:
                self.scene.find_rigid_body(collision_data["shape"]).deal_damage(1)
            set_to_die = True

        if set_to_die:
            self.scene.add_object(BulletBlast(self.body.position.x, self.body.position.y, (255, 230, 200)))
            self.scene.remove_object(self)