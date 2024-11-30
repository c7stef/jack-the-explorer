import pygame
import sys

import pickle

from button import Button, Dropdown, Checkbox, Slider, ControlsButton
from gameobject import OnScreen
from level import Level
import utils

class MainMenu(OnScreen):
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.set_screen_size()
        self.centered_button_x = self.screen_width / 2 - self.button_width / 2
        self.centered_button_y = self.screen_height / 2 - self.button_height / 2

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
        try:
            with open("controls.bin", "rb") as f:
                utils.controls = pickle.load(f)
        except FileNotFoundError:
            with open("controls.bin", "wb") as f:
                pickle.dump(utils.controls, f)

        self.font = pygame.font.SysFont("Arial", 20)
        options = []
        for opt in pygame.display.list_modes():
            if opt[0] < 600:
                continue
            options.append(str(opt[0]) + "x" + str(opt[1]))
        self.resolution_options = options
        self.back = mainMenu
        self.screen = mainMenu.screen
        self.old_conflicts = []
        self.pickResolution = "Resolution: "
        self.text_surface_res = self.font.render(self.pickResolution, True, (0, 0, 0))
        self.init_ui()

    def changeResolution(self, option):
        utils.controls['resolution'] = option
        self.init_ui()

    def init_ui(self):
        pygame.display.set_mode((int(utils.controls['resolution'].split("x")[0]), int(utils.controls['resolution'].split("x")[1])))
        self.set_screen_size()
        self.buttons = []
        self.drop_downs = []
        self.controls = []
        self.focused_element = None
        self.left_column_center_x = self.screen_width / 2 - self.screen_width / 4
        self.top_left_y = self.screen_height / 10
        self.button_right_column_center_x = self.screen_width / 2 + self.screen_width / 4 - self.button_width / 2
        self.button_right_column_first_y = self.screen_height / 10
        dropdown_x = self.left_column_center_x
        dropdown_y = self.top_left_y
        dropdown_width = self.screen_width / 8
        dropdown_height = self.screen_height / 18
        self.fullscreen_checkbox_y = self.top_left_y + dropdown_height + self.offset
        self.soundSlider_y = self.fullscreen_checkbox_y + self.offset + self.button_height
        options = self.resolution_options

        self.resolution = Dropdown(dropdown_x, dropdown_y, dropdown_width, dropdown_height, options, int(self.font_size / 1.5),
                                   (255, 255, 255), self.changeResolution, utils.controls['resolution'])
        self.text_pos_res = (dropdown_x - self.text_surface_res.get_width() - 10,
                             dropdown_y + dropdown_height / 2 - self.text_surface_res.get_height() / 2)
        self.buttons.append(Checkbox(self.left_column_center_x, self.fullscreen_checkbox_y, self.button_width,
                                     self.button_height, "Fullscreen", self.font_size, (0, 255, 0), self.toggleFullscreen))
        self.left = ControlsButton(self.button_right_column_center_x, self.button_right_column_first_y, self.button_width,
                                   self.button_height, "Left", self.font_size, (0, 255, 0), utils.controls, "left")
        self.right = ControlsButton(self.button_right_column_center_x, self.button_right_column_first_y + self.offset + self.button_height,
                                    self.button_width, self.button_height, "Right", self.font_size, (0, 255, 0), utils.controls, "right")
        self.up = ControlsButton(self.button_right_column_center_x, self.button_right_column_first_y + 2 * (self.offset + self.button_height),
                                 self.button_width, self.button_height, "Up", self.font_size, (0, 255, 0), utils.controls, "up")
        self.down = ControlsButton(self.button_right_column_center_x, self.button_right_column_first_y + 3 * (self.offset + self.button_height),
                                   self.button_width, self.button_height, "Down", self.font_size, (0, 255, 0), utils.controls, "down")
        self.soundSlider = Slider(self.left_column_center_x, self.soundSlider_y, self.button_width,
                                  self.button_height, (0, 255, 0), self.set_volume, "Volume: ", 20, utils.controls['sound'])
        self.goBack = Button(self.left_column_center_x, self.soundSlider_y + self.button_height + self.offset,
                             self.button_width, self.button_height, "Back", self.font_size, (0, 120, 0), self.backToMain)
        self.controls.append(self.left)
        self.controls.append(self.right)
        self.controls.append(self.up)
        self.controls.append(self.down)
        self.buttons.append(self.soundSlider)
        self.buttons.append(self.goBack)
        self.drop_downs.append(self.resolution)

    def toggleFullscreen(self, checked):
        pygame.display.toggle_fullscreen()

    def set_volume(self, volume):
        utils.controls['sound'] = volume

    def backToMain(self):
        with open("controls.bin", "wb") as f:
            pickle.dump(utils.controls, f)
        utils.currentScreen = MainMenu(self.screen)

    def handleInput(self):
        if self.focused_element is not None:
            ret = self.focused_element.handle_input(self.events)
            if ret is None:
                self.focused_element = None
            else: return
        for d in self.drop_downs:
            d.handle_input(self.events)
        for c in self.controls:
            ret = c.handle_input(self.events)
            if isinstance(ret, ControlsButton):
                self.focused_element = ret
                pass
        for b in self.buttons:
            b.handle_input()

    def update(self):
        self.handleInput()
        self.check_controls_conflicts()

    def check_controls_conflicts(self):
        conflict_found = False
        conflicts = []
        for c in self.controls:
            for c2 in self.controls:
                if c != c2 and c.controls[c.key] == c2.controls[c2.key]:
                    if c not in conflicts:
                        conflicts.append(c)
                    if c2 not in conflicts:
                        conflicts.append(c2)
                    conflict_found = True
        for c in conflicts:
            c.font_color = (255, 0, 0)

        if self.old_conflicts != conflicts:
            for c in self.old_conflicts:
                if c not in conflicts:
                    c.font_color = (0, 0, 0)
        self.old_conflicts = conflicts
        return conflict_found

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
        self.buttons = []
        self.set_screen_size()
        self.centered_button_x = self.screen_width / 2 - self.button_width / 2
        self.centered_button_y = self.screen_height / 2

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

