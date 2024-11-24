import pygame
import sys

from button import Button, Dropdown
from gameobject import OnScreen
from level import Level
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
        utils.currentScreen = LevelsMenu(self)

    def quitGame(self):
        pygame.quit()
        sys.exit()


    def settings(self):
        utils.currentScreen = Settings(self)
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

class Settings(OnScreen):
    def __init__(self, mainMenu):
        self.back = mainMenu
        self.screen = mainMenu.screen

        self.font = pygame.font.SysFont("Arial", 20)

        self.buttons = []

        self.goBack = Button(100, 400, 200, 50, "Back", 30, (0, 120, 0), self.backToMain)

        self.buttons.append(self.goBack)

        options = []

        for opt in pygame.display.list_modes():
            options.append(str(opt[0]) + "x" + str(opt[1]))

        self.pickResolution = "Resolution: "
        self.text_surface_res = self.font.render(self.pickResolution, True, (0, 0, 0))

        dropdown_x = 300
        dropdown_y = 100
        dropdown_width = 200
        dropdown_height = 50

        self.resolution = Dropdown(dropdown_x, dropdown_y, dropdown_width, dropdown_height,
                                   options, 20, (255, 255, 255), self.changeResolution)

        self.text_pos_res = (dropdown_x - self.text_surface_res.get_width() - 10,
                             dropdown_y + dropdown_height / 2 - self.text_surface_res.get_height() / 2)

        self.buttons.append(self.resolution)

    def changeResolution(self, option):
        width, height = option.split("x")
        pygame.display.set_mode((int(width), int(height)))

    def backToMain(self):
        utils.currentScreen = self.back

    def handleInput(self):
        for b in self.buttons:
            b.handle_input()

    def update(self):
        self.handleInput()

    def draw(self):
        for b in self.buttons:
            b.draw(self.screen)
        self.screen.blit(self.text_surface_res, self.text_pos_res)

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

