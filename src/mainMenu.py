import pygame
import sys

from button import Button
from gameobject import OnScreen

import utils

class MainMenu(OnScreen):
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start", "Quit", "Settings"]

        self.buttons = []

        self.start = Button(100, 100, 200, 50, "Start", 30, (0, 255, 0), self.startGame)
        self.quit = Button(100, 200, 200, 50, "Quit", 30, (255, 0, 0), self.quitGame)
        self.settings = Button(100, 300, 200, 50, "Settings", 30, (0, 0, 255), self.settings)

        self.buttons.append(self.start)
        self.buttons.append(self.quit)
        self.buttons.append(self.settings)

    def startGame(self):
        from levelsMenu import LevelsMenu
        utils.currentScreen = LevelsMenu(self)

    def quitGame(self):
        pygame.quit()
        sys.exit()


    def settings(self):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))

        for button in self.buttons:
            button.draw(self.screen)

    def handle_input(self):
        for button in self.buttons:
            button.handle_input()

    def update(self):
        self.handle_input()
