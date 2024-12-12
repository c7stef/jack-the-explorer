from gameobject import OnScreen, GameObject
from button import Button
import gun
import utils
import pickups

import pygame
import math

from image_processing import scale_surface_cover, scale_surface_contain

from animated_sprite import AnimatedSprite, HeartsBar, BulletIcons, bullet

backgrounds = {
    'game_over': pygame.image.load("assets/menu-backgrounds/game_over_resized.jpg"),
    'finished_level' : pygame.image.load("assets/menu-backgrounds/finished_level_resized.jpg"),
    'death': pygame.image.load("assets/menu-backgrounds/death.jpg")
}

class DisplayData(GameObject):
    def __init__(self, player):
        self.level = player.level
        self.font = pygame.font.Font("assets/fonts/Chewy-Regular.ttf", 40)
        self.color = (0, 0, 255)
        self.z_index = 100

        self.score = 0
        self.coin_cnt = 0
        self.mag_ammo = 0
        self.ammo = 0
        self.max_ammo = 0
        self.health = 0
        self.max_health = 0
        self.player = player

        self.bullet_icon = scale_surface_cover(bullet, (60, 60))
        self.coin_sprite = scale_surface_contain(pickups.coin_sprite, (54, 54))
        self.weapon_sprite = scale_surface_contain(pygame.transform.rotate(gun.weapon_sprite, 45), (54, 54))

        self.hearts_bar = HeartsBar(3, (30, 30))
        self.ammo_icons = BulletIcons(10, (60, 60))

    def update(self):
        self.score = self.level.score
        self.coin_cnt = self.level.coin_cnt
        self.ammo = self.level.equipped_weapon.current_ammo
        self.max_ammo = self.level.equipped_weapon.max_ammo
        self.health = self.level.hp
        self.max_health = self.level.max_hp
        self.mag_ammo = self.level.equipped_weapon.mag_ammo

        self.hearts_bar.update(self.player.lives, self.player.current_hp)
        self.ammo_icons.update(self.level)

    def draw(self, screen):
        coin_cnt = self.font.render(f"x{self.coin_cnt}", True, pygame.colordict.THECOLORS['white'])
        screen.blit(coin_cnt, (80, 16))
        screen.blit(self.coin_sprite, (26, 16))

        self.hearts_bar.draw(screen, (40, 78))

        total_ammo = self.font.render(f"x{self.ammo}", True, pygame.colordict.THECOLORS['white'])
        screen.blit(total_ammo, (80, 118))
        screen.blit(self.weapon_sprite, (26, 118))

        self.ammo_icons.draw(screen, (20, 166))

        def draw_arc(radius, color, circle_center, percent_done):
            circle_rect = pygame.Rect(circle_center[0] - radius, circle_center[1] - radius, radius * 2, radius * 2)
            pygame.draw.arc(screen, color, circle_rect, 0, 2 * math.pi * percent_done, 2)

        def reloading_animation():
            bullet_icon_pos = (150, 170)
            screen.blit(self.bullet_icon, bullet_icon_pos)

            percent_done = self.level.equipped_weapon.reload_history / self.level.equipped_weapon.RELOAD_TIME

            bullet_icon_center = (bullet_icon_pos[0] + self.bullet_icon.get_width() / 2, bullet_icon_pos[1] + self.bullet_icon.get_height() / 2)

            radius = self.bullet_icon.get_height() / 2 + 10
            draw_arc(radius, (75, 75, 75), bullet_icon_center, percent_done)
            radius += 2
            draw_arc(radius, (150, 150, 150), bullet_icon_center, percent_done)
            radius -= 4
            draw_arc(radius, (150, 150, 150), bullet_icon_center, percent_done)

        if self.level.equipped_weapon.is_reloading:
            reloading_animation()


class PauseScreen(OnScreen):
    def __init__(self, level):
        self.screen = level.scene.screen
        self.scene = level.scene
        self.level = level
        text = "Paused"
        self.set_screen_size()
        self.offset = self.screen_height / 100
        self.font = pygame.font.Font("assets/fonts/Chewy-Regular.ttf", self.font_size * 8)
        self.text_surface = self.font.render(text, True, (255, 0, 0))
        self.text_rec = self.text_surface.get_rect(center = (self.screen_width / 2, self.screen_height / 4.5))

        self.buttons = []

        self.center_button2_y = self.center_button_y + self.button_height + self.offset
        self.center_button3_y = self.center_button2_y + self.button_height + self.offset

        self.go_back_button = Button(self.center_button_x, self.center_button_y, self.button_width,
                                   self.button_height, "Continue", self.font_size, self.go_back)
        self.buttons.append(self.go_back_button)
        self.main_menu_button = Button(self.center_button_x, self.center_button3_y, self.button_width,
                                       self.button_height, "Main Menu", self.font_size, self.go_to_main_menu)
        self.buttons.append(self.main_menu_button)
        self.last_checkpoint_button = Button(self.center_button_x, self.center_button2_y, self.button_width,
                                             self.button_height, "Restart", self.font_size, self.last_checkpoint)
        self.buttons.append(self.last_checkpoint_button)

    def go_back(self):
        utils.current_screen = self.level

    def go_to_main_menu(self):
        from main_menu import MainMenu
        utils.current_screen = MainMenu(self.level.screen)

    def last_checkpoint(self):
        self.level.player.respawn()

        utils.current_screen = self.level

    def handle_input(self):
        for b in self.buttons:
            b.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and not utils.escape_pressed:
            utils.current_screen = self.level
            utils.escape_pressed = True
        if not keys[pygame.K_ESCAPE]:
            utils.escape_pressed = False

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
        self.set_screen_size()
        self.load_background(backgrounds["death"])
        utils.play_music(None)
        self.big_font_ratio = 0.35
        self.font_ratio = 0.05
        self.button_font_size = int(self.screen_height * self.font_ratio)

        font = pygame.font.Font("assets/fonts/Chewy-Regular.ttf", int(self.screen_height * self.big_font_ratio))
        text = "Wasted"
        self.text_surface = font.render(text, True, (255, 0, 0))
        self.text_rec = self.text_surface.get_rect(center = (level.scene.screen.get_width() / 2, level.scene.screen.get_height() / 2))
        self.screen.blit(self.text_surface, self.text_rec)

        self.button_y_bottom_left = self.screen_height - self.button_height - self.screen_height / 10
        self.button_x_bottom_left = self.screen_width / 20

        self.button_y_buttom_right = self.screen_height - self.button_height - self.screen_height / 10
        self.button_x_buttom_right = self.screen_width - self.button_width - self.screen_width / 20

        self.restart_button = Button(self.button_x_bottom_left * 1.3, self.button_y_bottom_left, self.button_width,
                                     self.button_height, "Restart", self.button_font_size, self.restart)
        self.last_button = Button(self.button_x_buttom_right / 1.1, self.button_y_buttom_right, self.button_width * 1.5,
                                  self.button_height, "Last Checkpoint", self.button_font_size, self.last_checkpoint)
        self.sound = pygame.mixer.Sound("sounds/u_are_dead.mp3")
        self.sound.set_volume(utils.controls['sound'])
        self.sound.play()

    def last_checkpoint(self):
        self.sound.stop()

        self.level.init_player_with_pistol()
        if self.checkpoint:
            self.level.player.body.position = self.checkpoint.body.position

        utils.current_screen = self.level

    def restart(self):
        self.sound.stop()

        for checkpoint in self.scene.find_objects_by_name("Checkpoint"):
            checkpoint.reset()

        self.level.init_player_with_pistol()

        utils.current_screen = self.level

    def handle_input(self):
        self.restart_button.update()
        self.last_button.update()

    def update(self):
        self.handle_input()

    def draw(self):
        self.draw_background()
        self.restart_button.draw(self.screen)
        self.last_button.draw(self.screen)
        self.screen.blit(self.text_surface, self.text_rec)


class FinishScreen(OnScreen):
    def __init__(self, level):
        self.scene = level.scene
        self.screen = level.scene.screen
        self.set_screen_size()
        utils.play_music(None)
        self.offset = self.screen_height / 10
        self.font_ratio = 0.12
        self.buttons = []
        self.level = level
        font = pygame.font.Font("assets/fonts/Chewy-Regular.ttf", int(self.screen_height * self.font_ratio))
        text = f"Level {self.level.num_level} completed"
        self.text_surface = font.render(text, True, (255, 255, 255))
        self.text_rec = self.text_surface.get_rect(center = (self.screen_width / 2, self.screen_height / 8))
        self.scene.remove_object(self.scene.find_player().display)
        self.scene.remove_object(self.scene.find_player())
        if level.num_level == 3:
            self.load_background(backgrounds['game_over'])
            self.restart_x = self.offset
            self.restart_y = self.screen_height - self.button_height - self.offset
            self.main_menu_button_y = self.restart_y
            self.main_menu_button_x = self.screen_width - self.button_width - self.offset
        else:
            self.load_background(backgrounds['finished_level'])
            self.restart_y = self.center_button_y - self.button_height - self.offset
            self.restart_x = self.center_button_x
            self.main_menu_button_y = self.center_button_y + self.button_height + self.offset
            self.main_menu_button_x = self.center_button_x
            self.next_level_button = Button(self.center_button_x, self.center_button_y,
                                        self.button_width, self.button_height, "Next Level", 40, self.next_level)
            self.buttons.append(self.next_level_button)

        self.restart_button = Button(self.restart_x, self.restart_y,
                                    self.button_width, self.button_height, "Restart", 40, self.restart)
        self.main_menu_button = Button(self.main_menu_button_x, self.main_menu_button_y,
                                    self.button_width, self.button_height, "Main Menu", 40, self.go_to_main_menu)
        self.buttons.append(self.restart_button)
        self.buttons.append(self.main_menu_button)

        self.sound = pygame.mixer.Sound("sounds/next_level.mp3")
        self.sound.set_volume(utils.controls['sound'])
        self.sound.play()

    def go_to_main_menu(self):
        self.sound.stop()

        from main_menu import MainMenu

        utils.current_screen = MainMenu(self.screen)

    def next_level(self):
        self.sound.stop()

        from level import Level

        utils.current_screen = Level(self.level.level_menu, self.level.num_level + 1)

    def restart(self):
        self.sound.stop()

        for checkpoint in self.scene.find_objects_by_name("Checkpoint"):
            checkpoint.reset()

        from level import Level

        utils.current_screen = Level(self.level.level_menu, self.level.num_level)

    def handle_input(self):
        for b in self.buttons:
            b.update()

    def update(self):
        self.handle_input()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.level.num_level != 3:
            self.screen.blit(self.text_surface, self.text_rec)
        for b in self.buttons:
            b.draw(self.screen)
