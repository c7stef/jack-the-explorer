from gameobject import OnScreen, GameObject
from button import Button
import utils

import pygame

from animatedSprite import AnimatedSprite, HeartsBar, BulletIcons
class DisplayData(GameObject):
    def __init__(self, player):
        self.level = player.level
        self.font = pygame.font.SysFont("Arial", 25)
        self.color = (0, 0, 255)
        self.score = 0
        self.coinCnt = 0
        self.magAmmo = 0
        self.ammo = 0
        self.maxAmmo = 0
        self.health = 0
        self.maxHealth = 0
        self.player = player

        self.coinAnimation = AnimatedSprite("assets/coin", (23, 23))

        self.heartsBar = HeartsBar(3, (30, 30))

        self.ammoIcons = BulletIcons(10, (23, 23))

    def update(self):
        self.score = self.level.score
        self.coinCnt = self.level.coinCnt
        self.ammo = self.level.equippedWeapon.currentAmmo
        self.maxAmmo = self.level.equippedWeapon.maxAmmo
        self.health = self.level.hp
        self.maxHealth = self.level.maxHp
        self.magAmmo = self.level.equippedWeapon.magAmmo

        self.coinAnimation.update()
        self.heartsBar.update(self.player.lives, self.player.current_hp)
        self.ammoIcons.update(self.level)

    def draw(self, screen):
        text = self.font.render(f"Score: {self.score} {self.coinCnt} Ammo: {self.magAmmo} / {self.ammo} (max: {self.maxAmmo}) HP: {self.player.current_hp} / {self.player.hp_per_life}", True, self.color)
        screen.blit(text, (0, 0))
        coinCnt = self.font.render(f"x{self.coinCnt}", True, self.color)
        screen.blit(coinCnt, (50, 25))
        self.coinAnimation.draw(screen, (34, 36))
        self.heartsBar.draw(screen, (25, 50))
        self.ammoIcons.draw(screen, (25, 100))


class PauseScreen(OnScreen):
    def __init__(self, level):
        self.screen = level.scene.screen
        self.scene = level.scene
        self.level = level
        self.font = pygame.font.SysFont("Arial", 225)
        text = "Paused"
        self.text_surface = self.font.render(text, True, (255, 0, 0))
        self.text_rec = self.text_surface.get_rect(center = (level.scene.screen.get_width() / 2, level.scene.screen.get_height() / 2))

        self.goBackButton = Button(100, 100, 150, 75, "Continue", 40, (0, 255, 255), self.goBack)

    def goBack(self):
        utils.currentScreen = self.level

    def handle_input(self):
        self.goBackButton.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and not utils.escapePressed:
            utils.currentScreen = self.level
            utils.escapePressed = True
        if not keys[pygame.K_ESCAPE]:
            utils.escapePressed = False

    def update(self):
        self.handle_input()

    def draw(self):
        self.scene.draw(self.screen)
        self.screen.blit(pygame.transform.grayscale(self.screen), (0, 0))
        self.screen.blit(self.text_surface, self.text_rec)
        self.goBackButton.draw(self.screen)

class DeathScreen(OnScreen):
    def __init__(self, level, checkpoint):
        self.screen = level.scene.screen
        self.scene = level.scene
        self.level = level
        self.checkpoint = checkpoint
        font = pygame.font.SysFont("Arial", 225)
        text = "Wasted"
        self.text_surface = font.render(text, True, (255, 0, 0))
        self.text_rec = self.text_surface.get_rect(center = (level.scene.screen.get_width() / 2, level.scene.screen.get_height() / 2))
        self.screen.blit(self.text_surface, self.text_rec)
        self.restart_button = Button(100, 100, 150, 75, "Restart", 40, (0, 255, 255), self.restart)
        self.last_button = Button(100, 200, 150, 75, "Last Checkpoint", 40, (0, 255, 255), self.last_checkpoint)
        self.sound = pygame.mixer.Sound("sounds/uAreDead.mp3")
        self.sound.play()

    def last_checkpoint(self):
        self.sound.stop()

        self.level.initPlayerWithPistol()
        if self.checkpoint:
            self.level.player.body.position = self.checkpoint.body.position

        utils.currentScreen = self.level

    def restart(self):
        self.sound.stop()

        for checkpoint in self.scene.find_objects_by_name("Checkpoint"):
            checkpoint.reset()

        self.level.initPlayerWithPistol()

        utils.currentScreen = self.level

    def handle_input(self):
        self.restart_button.update()
        self.last_button.update()

    def update(self):
        self.handle_input()

    def draw(self):
        self.screen.blit(pygame.transform.grayscale(self.screen), (0, 0))
        self.restart_button.draw(self.screen)
        self.last_button.draw(self.screen)
        self.screen.blit(self.text_surface, self.text_rec)
