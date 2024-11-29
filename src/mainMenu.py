import pygame
import sys

from button import Button, Dropdown, Checkbox, Slider, ControlsButton
from gameobject import OnScreen
from level import Level
import utils

class MainMenu(OnScreen):
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start", "Quit", "Settings"]

        self.buttons = []

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.button_width = self.screen_width / 5
        self.button_height = self.screen_height / 13
        self.centered_button_x = self.screen_width / 2 - self.button_width / 2
        self.centered_button_y = self.screen_height / 2 - self.button_height / 2

        self.font_ratio = 0.04
        self.font_size = int(self.screen_height * self.font_ratio)

        self.offset = self.screen_height / 18

        self.start = Button(self.centered_button_x, self.centered_button_y - self.button_height - self.offset, self.button_width
                            , self.button_height, "Start", self.font_size, (0, 255, 0), self.startGame)
        self.quit = Button(self.centered_button_x, self.centered_button_y + self.button_height + self.offset,
                           self.button_width, self.button_height, "Quit", self.font_size, (255, 0, 0), self.quitGame)
        self.settings = Button(self.centered_button_x, self.centered_button_y,
                               self.button_width, self.button_height, "Settings", self.font_size, (0, 0, 255), self.settings)

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
        self.controls = []

        self.drop_downs = []

        self.goBack = Button(100, 400, 200, 50, "Back", 30, (0, 120, 0), self.backToMain)

        self.left = ControlsButton(100, 20, 200, 50, "Left", 30, (0, 255, 0), utils.controls, "left")
        self.right = ControlsButton(350, 20, 200, 50, "Right", 30, (0, 255, 0), utils.controls, "right")
        self.up = ControlsButton(600, 20, 200, 50, "Up", 30, (0, 255, 0), utils.controls, "up")
        self.down = ControlsButton(850, 20, 200, 50, "Down", 30, (0, 255, 0), utils.controls, "down")

        self.buttons.append(self.goBack)
        self.controls.append(self.left)
        self.controls.append(self.right)
        self.controls.append(self.up)
        self.controls.append(self.down)

        options = []

        self.soundSlider = Slider(300, 200, 200, 50, (0, 255, 0), self.set_volume, "Volume: ", 20)

        self.buttons.append(self.soundSlider)

        for opt in pygame.display.list_modes():
            if opt[0] < 600:
                continue
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

        self.drop_downs.append(self.resolution)

        self.buttons.append(Checkbox(100, 300, 200, 50, "Fullscreen", 30, (0, 255, 0), self.toggleFullscreen))

        try:
            with open("settings.cfg", "r") as f:
                for line in f:
                    if "volume" in line:
                        self.soundSlider.set_value(float(line.split(":")[1]))
                    if "resolution" in line:
                        self.resolution.set_option(line.split(":")[1].strip())

        except FileNotFoundError:
            with open("settings.cfg", "w") as f:
                f.write("")

    def changeResolution(self, option):
        width, height = option.split("x")
        pygame.display.set_mode((int(width), int(height)))

    def toggleFullscreen(self, checked):
        pygame.display.toggle_fullscreen()

    def set_volume(self, volume):
        utils.volume = volume

    def backToMain(self):
        with open("settings.cfg", "w") as f:
            f.write("volume: " + str(utils.volume) + "\n")
            f.write("resolution: " + str(pygame.display.get_surface().get_width()) + "x" +
                    str(pygame.display.get_surface().get_height()) + "\n")
            f.write(f"left: {utils.K_LEFT}\n")
            f.write(f"right: {utils.K_RIGHT}\n")
            f.write(f"up: {utils.K_UP}\n")
            f.write(f"down: {utils.K_DOWN}\n")


        utils.currentScreen = MainMenu(self.screen)

    def handleInput(self):
        for d in self.drop_downs:
            d.handle_input(self.events)
        for c in self.controls:
            c.handle_input(self.events)
        for b in self.buttons:
            b.handle_input()

    def update(self):
        self.handleInput()

    def draw(self):
        for c in self.controls:
            c.draw(self.screen)
        for b in self.buttons:
            b.draw(self.screen)
        for d in self.drop_downs:
            d.draw(self.screen)
        self.screen.blit(self.text_surface_res, self.text_pos_res)

class LevelsMenu(OnScreen):
    def __init__(self, mainMenu):
        self.back = mainMenu
        self.screen = mainMenu.screen
        self.options = ["Level 1", "Level 2", "Level 3"]

        self.buttons = []

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.button_width = self.screen_width / 5
        self.button_height = self.screen_height / 13
        self.centered_button_x = self.screen_width / 2 - self.button_width / 2
        self.centered_button_y = self.screen_height / 2
        self.offset = self.screen_height / 18

        self.font_ratio = 0.04
        self.font_size = int(self.screen_height * self.font_ratio)

        self.level1 = Button(self.centered_button_x, self.centered_button_y - self.offset / 2 - self.offset - self.button_height * 2,
                             self.button_width, self.button_height, "Level 1", self.font_size, (0, 255, 0), self.startLevel1)
        self.level2 = Button(self.centered_button_x, self.centered_button_y - self.offset / 2 - self.button_height,
                             self.button_width, self.button_height, "Level 2", self.font_size, (255, 0, 0), self.startLevel2)
        self.level3 = Button(self.centered_button_x, self.centered_button_y + self.offset / 2, self.button_width,
                             self.button_height, "Level 3", self.font_size, (0, 0, 255), self.startLevel3)
        self.goBack = Button(self.centered_button_x, self.centered_button_y + self.offset / 2 + self.button_height + self.offset,
                             self.button_width, self.button_height, "Back", self.font_size, (0, 120, 0), self.backToMain)

        self.buttons.append(self.level1)
        self.buttons.append(self.level2)
        self.buttons.append(self.level3)
        self.buttons.append(self.goBack)

    def startLevel1(self):
        utils.currentScreen = Level(self, 1, (0, 255, 0))
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

