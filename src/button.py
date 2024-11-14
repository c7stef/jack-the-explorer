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