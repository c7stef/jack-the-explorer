import pygame

import utils

from bullet import Bullet
from gameobject import GameObject

class Weapon(GameObject):
    def __init__(self, level):
        self.level = level
        self.scene = level.scene
        self.player = level.player

        self.FIRE_RATE = 0
        self.RELOAD_TIME = 0

        self.bulletHistory = 0
        self.reloadHistory = 0
        self.magAmmo = 0
        self.currentAmmo = 0

        self.isEquipped = False
        self.isReloading = False
        self.reload_sound = pygame.mixer.Sound("sounds/reload.wav")
        self.reload_sound.set_volume(utils.controls['sound'])

    def reload(self):
        if self.magSize == self.magAmmo:
            return
        if self.isReloading:
            return
        self.isReloading = True
        self.reload_sound.play()
        self.reloadHistory = 0

    def updateAmmo(self):
        # Empty mag, enough ammo
        if self.magAmmo == 0 and self.currentAmmo >= self.magSize:
            self.magAmmo = self.magSize
            self.currentAmmo -= self.magSize
        # Not empty mag, enough ammo
        elif self.magAmmo < self.magSize and self.currentAmmo >= self.magSize - self.magAmmo:
            self.currentAmmo -= self.magSize - self.magAmmo
            self.magAmmo = self.magSize
        # Not enough ammo, empty mag
        elif self.currentAmmo < self.magSize and self.magAmmo == 0:
            self.magAmmo = self.currentAmmo
            self.currentAmmo = 0
        elif self.currentAmmo < self.magSize - self.magAmmo:
            self.magAmmo += self.currentAmmo
            self.currentAmmo = 0

    def fire(self):
        if self.bulletHistory >= self.FIRE_RATE and self.magAmmo > 0 and not self.isReloading:
            mouse_pos = pygame.mouse.get_pos()
            relativeBodyPos = self.scene.relative_position(self.player.body.position)
            relativeBulletDirection = mouse_pos - relativeBodyPos
            self.magAmmo -= 1

            self.scene.add_object(Bullet(self.player.body.position.x, self.player.body.position.y, relativeBulletDirection))
            self.bulletHistory = 0

    def update(self):
        self.bulletHistory += 1
        if self.isReloading:
            self.reloadHistory += 1
            if self.reloadHistory >= self.RELOAD_TIME:
                self.updateAmmo()
                self.isReloading = False
                self.reload_sound.stop()

    def equip(self):
        self.isEquipped = True

    def pickUpAmmo(self, ammo):
        self.currentAmmo += ammo
        if self.currentAmmo + ammo > self.maxAmmo:
            self.currentAmmo = self.maxAmmo

class Pistol(Weapon):
    def __init__(self, level):
        super().__init__(level)
        self.FIRE_RATE = 15
        self.RELOAD_TIME = 60
        self.damage = 1
        self.magSize = 5
        self.maxAmmo = 69
        self.currentAmmo = 15
        self.magAmmo = 5

    def draw(self, screen):
        # Add weapon model
        pass
