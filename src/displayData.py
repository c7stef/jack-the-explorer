from gameobject import OnScreen, GameObject
from button import Button
import utils

import pygame
import math

from imageProcessing import scale_surface

from animatedSprite import AnimatedSprite, HeartsBar, BulletIcons

bullet = pygame.image.load("assets/bullet/bullet.png")

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

        self.bulletIcon = scale_surface(bullet, (23, 23))

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

        def drawArc(radius, color, circle_center, percentDone):
            circleRect = pygame.Rect(circle_center[0] - radius, circle_center[1] - radius, radius * 2, radius * 2)
            pygame.draw.arc(screen, color, circleRect, 0, 2 * math.pi * percentDone, 2)

        def reloadingAnimation():
            bullet_icon_pos = (100, 100)
            screen.blit(self.bulletIcon, bullet_icon_pos)

            percentDone = self.level.equippedWeapon.reloadHistory / self.level.equippedWeapon.RELOAD_TIME

            bullet_icon_center = (bullet_icon_pos[0] + self.bulletIcon.get_width() / 2, bullet_icon_pos[1] + self.bulletIcon.get_height() / 2)

            radius = self.bulletIcon.get_height() / 2 + 10
            drawArc(radius, (75, 75, 75), bullet_icon_center, percentDone)
            radius += 2
            drawArc(radius, (150, 150, 150), bullet_icon_center, percentDone)
            radius -= 4
            drawArc(radius, (150, 150, 150), bullet_icon_center, percentDone)

        if self.level.equippedWeapon.isReloading:
            reloadingAnimation()


class PauseScreen(OnScreen):
    def __init__(self, level):
        self.screen = level.scene.screen
        self.scene = level.scene
        self.level = level
        self.font = pygame.font.SysFont("Arial", 225)
        text = "Paused"
        self.text_surface = self.font.render(text, True, (255, 0, 0))
        self.text_rec = self.text_surface.get_rect(center = (level.scene.screen.get_width() / 2, level.scene.screen.get_height() / 2))

        self.buttons = []

        self.goBackButton = Button(100, 100, 150, 75, "Continue", 40, (0, 255, 255), self.goBack)
        self.buttons.append(self.goBackButton)
        self.main_menu_button = Button(100, 200, 150, 75, "Main Menu", 40, (0, 255, 255), self.goToMainMenu)
        self.buttons.append(self.main_menu_button)
        self.restart_button = Button(100, 300, 150, 75, "Restart", 40, (0, 255, 255), self.restart)
        self.buttons.append(self.restart_button)
        self.last_checkpoint_button = Button(100, 400, 150, 75, "Last Checkpoint", 40, (0, 255, 255), self.last_checkpoint)
        self.buttons.append(self.last_checkpoint_button)

    def goBack(self):
        utils.currentScreen = self.level

    def goToMainMenu(self):
        utils.currentScreen = self.level.level_menu.back

    def restart(self):
        from level import Level
        utils.currentScreen = Level(self.level.level_menu, self.level.num_level, (0, 255, 0))

    def last_checkpoint(self):
        self.level.player.respawn()

        utils.currentScreen = self.level

    def handle_input(self):
        for b in self.buttons:
            b.update()

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
        for b in self.buttons:
            b.draw(self.screen)


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
        self.sound.set_volume(utils.volume)
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


class FinishScreen(OnScreen):
    def __init__(self, level):

        self.screen = level.scene.screen
        self.scene = level.scene

        self.scene.remove_object(self.scene.find_player().display)
        self.scene.remove_object(self.scene.find_player())

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.font_ratio = 0.08

        self.level = level
        font = pygame.font.SysFont("Arial", int(self.screen_height * self.font_ratio))
        text = f"Level {self.level.num_level} completed"
        self.text_surface = font.render(text, True, (50, 200, 50))
        self.text_rec = self.text_surface.get_rect(center = (self.screen_width / 2, self.screen_height / 8))

        self.buttons = []

        self.button_width = self.screen_width / 5
        self.button_height = self.screen_height / 13
        self.center_button_x = self.screen_width / 2 - self.button_width / 2
        self.center_button_y = self.screen_height / 2 - self.button_height / 2
        self.offset = self.screen_height / 10

        self.restart_button = Button(self.center_button_x, self.center_button_y - self.button_height - self.offset,
                                     self.button_width, self.button_height, "Restart", 40, (0, 255, 255), self.restart)
        self.main_menu_button = Button(self.center_button_x, self.center_button_y + self.button_height + self.offset,
                                       self.button_width, self.button_height, "Main Menu", 40, (0, 255, 255), self.goToMainMenu)
        self.next_level_button = Button(self.center_button_x, self.center_button_y,
                                        self.button_width, self.button_height, "Next Level", 40, (0, 255, 255), self.nextLevel)

        self.buttons.append(self.restart_button)
        self.buttons.append(self.main_menu_button)
        self.buttons.append(self.next_level_button)

        self.sound = pygame.mixer.Sound("sounds/nextLevel.mp3")
        self.sound.set_volume(utils.volume)
        self.sound.play()

    def goToMainMenu(self):
        self.sound.stop()

        utils.currentScreen = self.level.level_menu.back

    def nextLevel(self):
        self.sound.stop()

        from level import Level

        utils.currentScreen = Level(self.level.level_menu, self.level.num_level + 1, (0, 255, 0))

    def restart(self):
        self.sound.stop()

        for checkpoint in self.scene.find_objects_by_name("Checkpoint"):
            checkpoint.reset()

        from level import Level

        utils.currentScreen = Level(self.level.level_menu, self.level.num_level, (0, 255, 0))

    def handle_input(self):
        for b in self.buttons:
            b.update()

    def update(self):
        self.handle_input()

    def draw(self):
        self.screen.blit(pygame.transform.grayscale(self.screen), (0, 0))

        for b in self.buttons:
            b.draw(self.screen)

        self.screen.blit(self.text_surface, self.text_rec)