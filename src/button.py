import pygame

from gameobject import GameObject

from imageProcessing import scale_surface

mousePressed = False

tick = pygame.image.load("assets/tick/tick.png")

class Button(GameObject):
    def __init__(self, x, y, width, height, text, font_size, color, on_click):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = color
        self.on_click = on_click

    def handle_input(self):
        global mousePressed
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not mousePressed:
                self.on_click()
                mousePressed = True
        if not pygame.mouse.get_pressed()[0]:
            mousePressed = False

    def update(self):
        self.handle_input()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class Dropdown(GameObject):
    def __init__(self, x, y, width, height, options, font_size, color, on_select):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = color
        self.border_color = (0, 0, 0)
        self.on_select = on_select
        self.selected_option = None
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

    def handle_input(self, events):
        global mousePressed
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
                if pygame.mouse.get_pressed()[0] and not mousePressed:
                    if mouse_pos[1] < self.rect.y:
                        self.scroll_offset = max(self.scroll_offset - 1, 0)
                    elif mouse_pos[1] > self.rect.y + self.rect.height:
                        self.scroll_offset = min(self.scroll_offset + 1, len(self.options) - self.max_visible_options)
                    mousePressed = True

            for i in range(self.max_visible_options):
                option_index = i + self.scroll_offset
                if option_index >= len(self.options):
                    break
                option = self.options[option_index]
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height,
                                          self.rect.width, self.option_height)
                if option_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not mousePressed:
                    self.selected_option = option
                    self.on_select(option)
                    self.is_open = False

        if not pygame.mouse.get_pressed()[0]:
            mousePressed = False

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not mousePressed:
                self.is_open = not self.is_open
                mousePressed = True
        else:
            if pygame.mouse.get_pressed()[0] and not mousePressed:
                self.is_open = False
                mousePressed = True

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
                option_text_surface = self.font.render(option, True, (0, 0, 0))
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


class Checkbox(GameObject):
    def __init__(self, x, y, width, height, text, font_size, color, on_click):
        self.rect = pygame.Rect(x + height + 5, y, width, height)
        self.rectSquare = pygame.Rect(x, y, height, height)
        self.text = text
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = color
        self.border_color = (0, 0, 0)
        self.on_click = on_click
        self.is_checked = False
        self.tick = scale_surface(tick, (height, height))

    def handle_input(self):
        global mousePressed
        mouse_pos = pygame.mouse.get_pos()
        if self.rectSquare.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not mousePressed:
                self.is_checked = not self.is_checked
                self.on_click(self.is_checked)
                mousePressed = True
        if not pygame.mouse.get_pressed()[0]:
            mousePressed = False

    def update(self):
        self.handle_input()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (240, 240, 240), self.rectSquare)
        pygame.draw.rect(screen, self.border_color, self.rectSquare, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        if self.is_checked:
            screen.blit(self.tick, self.rectSquare.topleft)
