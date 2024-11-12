from gameobject import GameObject

import pygame

class DisplayData(GameObject):
    def __init__(self, player):
        self.scene = player.scene
        self.screen = self.scene.screen
        self.font = pygame.font.SysFont("Arial", 25)
        self.color = (0, 0, 255)
        self.score = 0
        self.coinCnt = 0
        self.ammo = 0
        self.player = player

    def update(self):
        self.score = self.player.score
        self.coinCnt = self.player.coinCnt
        self.ammo = self.player.currentAmmo
        self.maxAmmo = self.player.maxAmmo

    def draw(self, screen):
        text = self.font.render(f"Score: {self.score} Coins: {self.coinCnt} Ammo: {self.ammo} / {self.maxAmmo}", True, self.color)
        screen.blit(text, (0, 0))