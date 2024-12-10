import pygame

from gameobject import GameObject, ImageObject

from image_processing import scale_surface

import utils

mouse_pressed = False
button_text_color = (1, 60, 100)

tick = pygame.image.load("assets/tick/tick.png")

button_default = {
'default' : pygame.image.load("assets/buttons/button1.png"),
'hover' : pygame.image.load("assets/buttons/button1_hover.png")
}

slider_default = {
'default' : pygame.image.load("assets/buttons/slider1.png"),
'hover' : pygame.image.load("assets/buttons/slider1.png")
}

button_backgrounds = {
    'default' : button_default,
    'slider' : slider_default
}

class Button(ImageObject):
    def __init__(self, x, y, width, height, text, font_size, color, on_click, button_type='default'):
        self.rect = pygame.Rect(x, y, width, height)
        super().__init__(self.rect, width, height, button_backgrounds[button_type])
        self.text = text
        self.font = utils.ui_font
        self.color = color
        self.on_click = on_click

        self.hover_color = ( min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255))

    def handle_input(self):
        global mouse_pressed
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
            if pygame.mouse.get_pressed()[0] and not mouse_pressed:
                self.on_click()
                mouse_pressed = True
        else:
            self.hover = False
        if not pygame.mouse.get_pressed()[0]:
            mouse_pressed = False

    def update(self):
        self.handle_input()

    def draw(self, screen):
        super().draw(screen)
        text_surface = self.font.render(self.text, True, button_text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class ControlsButton(Button):
    def __init__(self, x, y, width, height, text, font_size, color, controls, key):
        super().__init__(x, y, width, height, text, font_size, color, None)
        text_rect = pygame.Rect(x - width, y, width, height)
        self.text_surface = self.font.render(text, True, pygame.colordict.THECOLORS['white'])
        self.text_rect = self.text_surface.get_rect(center=text_rect.center)
        self.controls = controls
        self.key = key
        self.selected = False
        self.text = pygame.key.name(controls[key])

    def update_text(self, text):
        self.controls[self.key] = text
        self.text = pygame.key.name(self.controls[self.key])

    def handle_input(self, events):
        global mouse_pressed
        self.is_selected()
        ret = None
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.hover = True
                    self.selected = True
                else:
                    self.hover = False
            if e.type == pygame.KEYDOWN and self.selected:
                if e.key is pygame.K_ESCAPE:
                    self.selected = False
                    break
                self.text = pygame.key.name(e.key)
                self.controls[self.key] = e.key
                self.selected = False
        if self.selected:
            return self
        return ret

    def is_selected(self):
        if self.selected:
            if self.text[0] != ">":
                self.text = f"> {self.text} <"
        else:
            if self.text[0] == ">":
                self.text = self.text[2:-2]

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.text_surface, self.text_rect)

class Dropdown(GameObject):
    def __init__(self, x, y, width, height, options, font_size, color, on_select, selected_option=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = color
        self.border_color = (0, 0, 0)
        self.on_select = on_select
        self.selected_option = selected_option
        self.is_open = False
        self.border_thickness = 2
        self.border_rect = pygame.Rect(x - self.border_thickness, y - self.border_thickness,
                                       width + 2 * self.border_thickness,height + 2 * self.border_thickness)

        self.scroll_down_rect =  pygame.Rect(x, y + height, width, 15)

        self.scroll_up_rect = pygame.Rect(x, y - 15 , width, 15)

        self.scroll_offset = 0
        self.max_visible_options = 5
        self.option_height = height

        self.scroll_speed = 15
        self.scroll_history = 0

    def set_option(self, option):
        self.selected_option = option
        self.on_select(option)

    def handle_input(self, events):
        global mouse_pressed
        mouse_pos = pygame.mouse.get_pos()

        if self.scroll_down_rect.collidepoint(mouse_pos):
            self.scroll_history += 1
            if self.scroll_history >= self.scroll_speed:
                self.scroll_history = 0
                self.scroll_offset = min(self.scroll_offset + 1, len(self.options) - self.max_visible_options)

        if self.scroll_up_rect.collidepoint(mouse_pos):
            self.scroll_history += 1
            if self.scroll_history >= self.scroll_speed:
                self.scroll_history = 0
                self.scroll_offset = max(self.scroll_offset - 1, 0)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scroll_offset = max(self.scroll_offset - 1, 0)
                elif event.button == 5:
                    self.scroll_offset = min(self.scroll_offset + 1, len(self.options) - self.max_visible_options)

        if self.is_open:
            if self.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] and not mouse_pressed:
                    if mouse_pos[1] < self.rect.y:
                        self.scroll_offset = max(self.scroll_offset - 1, 0)
                    elif mouse_pos[1] > self.rect.y + self.rect.height:
                        self.scroll_offset = min(self.scroll_offset + 1, len(self.options) - self.max_visible_options)
                    mouse_pressed = True

            for i in range(self.max_visible_options):
                option_index = i + self.scroll_offset
                if option_index >= len(self.options):
                    break
                option = self.options[option_index]
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height,
                                          self.rect.width, self.option_height)
                if option_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not mouse_pressed:
                    self.selected_option = option
                    self.on_select(option)
                    self.is_open = False
                    mouse_pressed = True
        if not pygame.mouse.get_pressed()[0]:
            mouse_pressed = False

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not mouse_pressed:
                self.is_open = not self.is_open
                mouse_pressed = True
        else:
            if pygame.mouse.get_pressed()[0] and not mouse_pressed:
                self.is_open = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.border_color, self.border_rect)
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.selected_option if self.selected_option else "Select", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        if self.is_open:
            for i in range(self.max_visible_options):
                option_index = i + self.scroll_offset
                if option_index >= len(self.options):
                    break
                option = self.options[option_index]
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height,
                                            self.rect.width, self.option_height)
                option_rect_border = pygame.Rect(option_rect.x - self.border_thickness,
                                                    option_rect.y - self.border_thickness, option_rect.width + 2 * self.border_thickness,
                                                    option_rect.height + 2 * self.border_thickness)
                pygame.draw.rect(screen, self.border_color, option_rect_border)
                pygame.draw.rect(screen, self.color, option_rect)
                option_text_surface = self.font.render(option, True, pygame.colordict.THECOLORS['white'])
                option_text_rect = option_text_surface.get_rect(center=option_rect.center)
                screen.blit(option_text_surface, option_text_rect)

            # Draw scroll indicators
            if self.scroll_offset > 0:
                pygame.draw.polygon(screen, self.border_color, [(self.rect.x + self.rect.width // 2, self.rect.y - 10),
                                                                (self.rect.x + self.rect.width // 2 - 5, self.rect.y - 5),
                                                                (self.rect.x + self.rect.width // 2 + 5, self.rect.y - 5)])
            if self.scroll_offset < len(self.options) - self.max_visible_options:
                pygame.draw.polygon(screen, self.border_color, [(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height + 10),
                                                                        (self.rect.x + self.rect.width // 2 - 5, self.rect.y + self.rect.height + 5),
                                                                (self.rect.x + self.rect.width // 2 + 5, self.rect.y + self.rect.height + 5)])

    def update(self):
        self.handle_input()


class Checkbox(ImageObject):
    def __init__(self, x, y, width, height, text, font_size, color, on_click, initial_state=False, defaultImg='slider'):
        self.rect = pygame.Rect(x, y, width, height)
        super().__init__(self.rect, width, height, button_backgrounds[defaultImg])
        self.rect_square = pygame.Rect(x - height, y + height / 4, height / 2, height / 2)
        self.text = text
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = color
        self.border_color = (0, 0, 0)
        self.on_click = on_click
        self.is_checked = initial_state
        self.tick = scale_surface(tick, (height / 2, height / 2))

    def handle_input(self):
        global mouse_pressed
        mouse_pos = pygame.mouse.get_pos()
        if self.rect_square.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not mouse_pressed:
                self.is_checked = not self.is_checked
                self.on_click()
                mouse_pressed = True
        if not pygame.mouse.get_pressed()[0]:
            mouse_pressed = False

    def update(self):
        self.handle_input()

    def draw(self, screen):
        super().draw(screen)
        # pygame.draw.rect(screen, self.color, self.rect)
        # pygame.draw.rect(screen, (240, 240, 240), self.rect_square)
        pygame.draw.rect(screen, self.border_color, self.rect_square, 2)
        text_surface = self.font.render(self.text, True, pygame.colordict.THECOLORS['white'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        if self.is_checked:
            screen.blit(self.tick, self.rect_square.topleft)


class Slider(ImageObject):
    def __init__(self, x, y, width, height, color, on_change, text, font_size, default_value=0.5, image_type='slider'):
        self.rect = pygame.Rect(x, y, width, height)
        super().__init__(self.rect, width + 80, height, button_backgrounds[image_type])

        self.font = pygame.font.SysFont("Arial", font_size)
        self.text = text

        self.color = color
        self.border_color = (0, 0, 0)
        self.on_change = on_change
        self.value = default_value
        self.is_dragging = False

    def set_value(self, value):
        self.value = value
        self.on_change(value)

    def handle_input(self):
        global mouse_pressed
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not mouse_pressed:
                self.is_dragging = True
                mouse_pressed = True
        if not pygame.mouse.get_pressed()[0]:
            self.is_dragging = False
            mouse_pressed = False

        if self.is_dragging:
            self.value = (mouse_pos[0] - self.rect.x) / self.rect.width
            self.value = min(max(self.value, 0), 1)
            self.on_change(self.value)

    def update(self):
        self.handle_input()

    def draw(self, screen):
        super().draw(screen)

        text_surface = self.font.render(self.text, True, pygame.colordict.THECOLORS['white'])
        text_rect = text_surface.get_rect(center=(self.rect.x - text_surface.get_width() / 2 - self.rect.x / 13 , self.rect.y + self.rect.height / 2))
        screen.blit(text_surface, text_rect)

        percent_text_surface = self.font.render(str(int(self.value * 100)) + "%", True, pygame.colordict.THECOLORS['white'])
        percent_text_rect = percent_text_surface.get_rect(center=(self.rect.x + self.rect.width + percent_text_surface.get_width() / 2 + self.rect.x / 13, self.rect.y + self.rect.height / 2))
        screen.blit(percent_text_surface, percent_text_rect)

        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x + self.value * self.rect.width - 4, self.rect.y, 8, self.rect.height))
