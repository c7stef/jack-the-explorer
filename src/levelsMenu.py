import pygame

from button import Button
from gameobject import OnScreen
from level import Level

import utils

class LevelsMenu(OnScreen):
    def __init__(self, mainMenu):
        self.back = mainMenu
        self.screen = mainMenu.screen
        self.options = ["Level 1", "Level 2", "Level 3"]

        self.buttons = []

        self.level1 = Button(100, 100, 200, 50, "Level 1", 30, (0, 255, 0), self.startLevel1)
        self.level2 = Button(100, 200, 200, 50, "Level 2", 30, (255, 0, 0), self.startLevel2)
        self.level3 = Button(100, 300, 200, 50, "Level 3", 30, (0, 0, 255), self.startLevel3)

        self.goBack = Button(100, 400, 200, 50, "Back", 30, (0, 120, 0), self.backToMain)

        self.buttons.append(self.level1)
        self.buttons.append(self.level2)
        self.buttons.append(self.level3)
        self.buttons.append(self.goBack)

    def startLevel1(self):
        utils.currentScreen = Level(self.screen, 0, (0, 255, 0))
        pass

    def startLevel2(self):
        pass

    def startLevel3(self):
        pass

    def backToMain(self):
        utils.currentScreen = self.back

    def draw(self):
        self.screen.fill((255, 255, 255))

        for button in self.buttons:
            button.draw(self.screen)

    def handle_input(self):
        for button in self.buttons:
            button.handle_input()

    def update(self):
        self.handle_input()