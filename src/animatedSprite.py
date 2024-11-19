import pygame

from PIL import Image

coinSprite = []

coinBlinkYes = pygame.image.load("assets/coin/blink/white.png")
coinSprite.append(coinBlinkYes)

coinBlinkNo = pygame.image.load("assets/coin/blink/normal.png")
coinSprite.append(coinBlinkNo)

coinStates = ["/rotate", "/shine"]
for c in coinStates:
    for i in range(1, 7):
        coinSprite.append(pygame.image.load("assets/coin" + c + "/" + str(i) + ".png"))

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, path, scale=None):
        super().__init__()

        self.frames = []
        self.frameCnt = 0
        self.currentFrame = 0

        if path == "assets/coin":
            self.frames = coinSprite
        else:
            print("Error: No such defined path")

        if scale is not None:
            for i in range(len(self.frames)):
                self.frames[i] = pygame.transform.scale(self.frames[i], scale)

    def update(self):
        self.frameCnt += 1
        if self.frameCnt >= 8:
            self.frameCnt = 0
            self.currentFrame = (self.currentFrame + 1) % len(self.frames)

    def draw(self, screen, position):
        screen.blit(self.frames[self.currentFrame], position)
