from gameobject import GameObject
import pygame
from button import Button

class DeathScreen(GameObject):
    def __init__(self, scene):
        self.screen = scene.screen
        self.scene = scene
        font = pygame.font.SysFont("Arial", 225)
        text = "Wasted"
        self.text_surface = font.render(text, True, (255, 0, 0))
        self.text_rec = self.text_surface.get_rect(center = (scene.screen.get_width() / 2, scene.screen.get_height() / 2))
        self.screen.blit(self.text_surface, self.text_rec)
        self.restart_button = Button(100, 100, 150, 75, "Restart", 40, (0, 255, 255), self.restart)
        # self.scene.add_object(self.restart_button)
        self.scene.add_object(self)

    def restart(self):
        self.delete()
        from player import Player
        self.scene.add_object(Player(100, 100))

    def delete(self):
        self.scene.remove_object(self)
        # self.scene.remove_object(self.restart_button)

    def handle_input(self):
        pass

    def update(self):
        self.restart_button.update()
        pass

    def draw(self, screen):
        screen.blit(pygame.transform.grayscale(screen), (0, 0))
        self.restart_button.draw(screen)
        screen.blit(self.text_surface, self.text_rec)
        # screen.blit(self.restart_button, self.restart_button.rect)