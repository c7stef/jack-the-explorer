import pygame

from gameobject import GameObject

mousePressed = False

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

    def handle_input(self):
        global mousePressed
        mouse_pos = pygame.mouse.get_pos()

        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                          self.rect.width, self.rect.height)
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
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                          self.rect.width, self.rect.height)
                option_rect_border = pygame.Rect(option_rect.x - self.border_thickness,
                                                 option_rect.y - self.border_thickness, option_rect.width + 2 * self.border_thickness,
                                                 option_rect.height + 2 * self.border_thickness)
                pygame.draw.rect(screen, self.border_color, option_rect_border)
                pygame.draw.rect(screen, self.color, option_rect)
                option_text_surface = self.font.render(option, True, (0, 0, 0))
                option_text_rect = option_text_surface.get_rect(center=option_rect.center)
                screen.blit(option_text_surface, option_text_rect)

    def update(self):
        self.handle_input()