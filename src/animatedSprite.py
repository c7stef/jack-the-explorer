import pygame

from imageProcessing import scale_surface

coinSprite = []

coinBlinkYes = pygame.image.load("assets/coin/blink/white.png")
coinSprite.append(coinBlinkYes)

coinBlinkNo = pygame.image.load("assets/coin/blink/normal.png")
coinSprite.append(coinBlinkNo)

coinStates = ["/rotate", "/shine"]
for c in coinStates:
    for i in range(1, 7):
        coinSprite.append(pygame.image.load("assets/coin" + c + "/" + str(i) + ".png"))

fullHeart = pygame.image.load("assets/heart/full.png")
halfHeart = pygame.image.load("assets/heart/half.png")
emptyHeart = pygame.image.load("assets/heart/empty.png")

bullet = pygame.image.load("assets/bullet/bullet.png")

class AnimatedSprite():
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
                self.frames[i] = scale_surface(self.frames[i], scale)

    def update(self):
        self.frameCnt += 1
        if self.frameCnt >= 8:
            self.frameCnt = 0
            self.currentFrame = (self.currentFrame + 1) % len(self.frames)

    def draw(self, screen, position):
        frame = self.frames[self.currentFrame]
        screen.blit(frame, position - pygame.Vector2(frame.get_size()) / 2)


class HeartsBar():
    def __init__(self, nrHearts, scale=None):
        super().__init__()

        self.spacing = 30

        self.nrHearts = nrHearts
        self.hp_per_heart = 3
        self.current_hp = nrHearts * self.hp_per_heart

        self.fullHeart = fullHeart
        self.halfHeart = halfHeart
        self.emptyHeart = emptyHeart

        if scale:
            self.fullHeart = pygame.transform.scale(self.fullHeart, scale)
            self.halfHeart = pygame.transform.scale(self.halfHeart, scale)
            self.emptyHeart = pygame.transform.scale(self.emptyHeart, scale)

            self.spacing = scale[0] + 5

    def update(self, lives, current_hp):
        self.nrHearts = lives
        self.current_hp = current_hp


    def draw(self, screen, position):
        for i in range(self.nrHearts):
            current_heart_hp = self.current_hp - i * self.hp_per_heart
            if current_heart_hp >= self.hp_per_heart:
                screen.blit(self.fullHeart, (position[0] + self.spacing * i, position[1]))
            elif current_heart_hp > 0:
                screen.blit(self.halfHeart, (position[0] + self.spacing * i, position[1]))
            else:
                screen.blit(self.fullHeart, (position[0] + self.spacing * i, position[1]))



class BulletIcons():
    def __init__(self, nrBullets, scale=None):
        self.spacing = 10
        self.maxNrBullets = nrBullets
        self.nrBullets = 0
        self.bullet = bullet

        if scale:
            self.bullet = scale_surface(self.bullet, scale)
            self.spacing = scale[0] + 5

    def update(self, level):
        self.magAmmo = level.equippedWeapon.magAmmo
        if self.nrBullets > self.magAmmo:
            self.nrBullets = self.magAmmo
        if self.nrBullets < self.magAmmo:
            self.nrBullets = self.magAmmo
            if self.nrBullets > self.maxNrBullets:
                self.nrBullets = self.maxNrBullets

    def draw(self, screen, position):
        for i in range(self.nrBullets):
            screen.blit(self.bullet, (position[0] + 10 * i, position[1]))