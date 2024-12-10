import pygame

import utils

from bullet import Bullet
from gameobject import GameObject

weapon_sprite = pygame.image.load("assets/weapon/weapon.png")

class Weapon(GameObject):
    def __init__(self, level):
        self.level = level
        self.scene = level.scene
        self.player = level.player

        self.FIRE_RATE = 0
        self.RELOAD_TIME = 0

        self.bullet_history = 0
        self.reload_history = 0
        self.mag_ammo = 0
        self.current_ammo = 0

        self.is_equipped = False
        self.is_reloading = False
        self.reload_sound = pygame.mixer.Sound("sounds/reload.wav")
        self.reload_sound.set_volume(utils.controls['sound'])

    def reload(self):
        if self.mag_size == self.mag_ammo:
            return
        if self.is_reloading:
            return
        self.is_reloading = True
        self.reload_sound.play()
        self.reload_history = 0

    def update_ammo(self):
        # Empty mag, enough ammo
        if self.mag_ammo == 0 and self.current_ammo >= self.mag_size:
            self.mag_ammo = self.mag_size
            self.current_ammo -= self.mag_size
        # Not empty mag, enough ammo
        elif self.mag_ammo < self.mag_size and self.current_ammo >= self.mag_size - self.mag_ammo:
            self.current_ammo -= self.mag_size - self.mag_ammo
            self.mag_ammo = self.mag_size
        # Not enough ammo, empty mag
        elif self.current_ammo < self.mag_size and self.mag_ammo == 0:
            self.mag_ammo = self.current_ammo
            self.current_ammo = 0
        elif self.current_ammo < self.mag_size - self.mag_ammo:
            self.mag_ammo += self.current_ammo
            self.current_ammo = 0

    def fire(self):
        if self.bullet_history >= self.FIRE_RATE and self.mag_ammo > 0 and not self.is_reloading:
            mouse_pos = pygame.mouse.get_pos()
            relative_body_pos = self.scene.relative_position(self.player.body.position)
            relative_bullet_direction = mouse_pos - relative_body_pos
            self.mag_ammo -= 1

            self.scene.add_object(Bullet(self.player.body.position.x, self.player.body.position.y, relative_bullet_direction))
            self.bullet_history = 0

    def update(self):
        self.bullet_history += 1
        if self.is_reloading:
            self.reload_history += 1
            if self.reload_history >= self.RELOAD_TIME:
                self.update_ammo()
                self.is_reloading = False
                self.reload_sound.stop()

    def equip(self):
        self.is_equipped = True

    def pick_up_ammo(self, ammo):
        self.current_ammo += ammo
        if self.current_ammo + ammo > self.max_ammo:
            self.current_ammo = self.max_ammo

class Pistol(Weapon):
    def __init__(self, level):
        super().__init__(level)
        self.FIRE_RATE = 15
        self.RELOAD_TIME = 60
        self.damage = 1
        self.mag_size = 5
        self.max_ammo = 69
        self.current_ammo = 15
        self.mag_ammo = 5

    def draw(self, screen):
        # Add weapon model
        pass
