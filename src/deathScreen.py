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
        self.scene.add_object(self)
        self.playerCnt = 0
        self.sound = pygame.mixer.Sound("sounds/uAreDead.mp3")
        self.sound.play()


    def restart(self):
        self.sound.stop()
        self.delete()
        from player import Player
        import utils
        if self.playerCnt == 0:
            self.playerCnt += 1
            utils.player = Player(100, 100)
            self.scene.add_object(utils.player)

    def delete(self):
        self.scene.remove_object(self)

    def handle_input(self):
        pass

    def update(self):
        self.restart_button.update()

    def draw(self, screen):
        screen.blit(pygame.transform.grayscale(screen), (0, 0))
        self.restart_button.draw(screen)
        screen.blit(self.text_surface, self.text_rec)
