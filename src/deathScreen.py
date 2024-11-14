from gameobject import OnScreen
import pygame
import utils
from button import Button

class DeathScreen(OnScreen):
    def __init__(self, level):
        self.screen = level.scene.screen
        self.scene = level.scene
        self.level = level
        font = pygame.font.SysFont("Arial", 225)
        text = "Wasted"
        self.text_surface = font.render(text, True, (255, 0, 0))
        self.text_rec = self.text_surface.get_rect(center = (level.scene.screen.get_width() / 2, level.scene.screen.get_height() / 2))
        self.screen.blit(self.text_surface, self.text_rec)
        self.restart_button = Button(100, 100, 150, 75, "Restart", 40, (0, 255, 255), self.restart)
        self.playerCnt = 0
        self.sound = pygame.mixer.Sound("sounds/uAreDead.mp3")
        self.sound.play()

    def restart(self):
        self.sound.stop()

        from player import Player

        self.level.player = Player(100, 100, self.level)
        self.scene.add_object(self.level.player)

        utils.currentScreen = self.level

    def handle_input(self):
        self.restart_button.update()

    def update(self):
        self.handle_input()

    def draw(self):
        self.screen.blit(pygame.transform.grayscale(self.screen), (0, 0))
        self.restart_button.draw(self.screen)
        self.screen.blit(self.text_surface, self.text_rec)
