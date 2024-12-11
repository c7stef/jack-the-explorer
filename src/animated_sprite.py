import pygame
import os

from image_processing import scale_surface_cover, scale_surface_contain

full_heart = pygame.image.load("assets/heart/full.png")
half_heart = pygame.image.load("assets/heart/half.png")
empty_heart = pygame.image.load("assets/heart/empty.png")

bullet = pygame.transform.rotate(pygame.image.load("assets/bullet/bullet.png"), 45)

class AnimatedSprite():
    def __init__(self, path, scale=None, frame_duration=8):
        super().__init__()

        self.path = path
        self.frames = []
        self.frame_cnt = 0
        self.current_frame = 0
        self.frame_duration = frame_duration

        self.frames = [
            pygame.image.load(os.path.join(path, f))
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ]

        if scale is not None:
            for i in range(len(self.frames)):
                self.frames[i] = scale_surface_contain(self.frames[i], scale)

    def flipped(self):
        new_sprite = AnimatedSprite(self.path, frame_duration=self.frame_duration)
        new_sprite.frames = [pygame.transform.flip(f, True, False) for f in self.frames]
        return new_sprite

    def update(self):
        self.frame_cnt += 1
        if self.frame_cnt >= self.frame_duration:
            self.frame_cnt = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen, position):
        frame = self.frames[self.current_frame]
        screen.blit(frame, position - pygame.Vector2(frame.get_size()) / 2)

class HeartsBar():
    def __init__(self, nr_hearts, scale=None):
        super().__init__()

        self.spacing = 40

        self.nr_hearts = nr_hearts
        self.hp_per_heart = 3
        self.current_hp = nr_hearts * self.hp_per_heart

        self.full_heart = full_heart
        self.half_heart = half_heart
        self.empty_heart = empty_heart

        if scale:
            self.full_heart = pygame.transform.scale(self.full_heart, scale)
            self.half_heart = pygame.transform.scale(self.half_heart, scale)
            self.empty_heart = pygame.transform.scale(self.empty_heart, scale)

            self.spacing = scale[0] + 5

    def update(self, lives, current_hp):
        self.nr_hearts = lives
        self.current_hp = current_hp


    def draw(self, screen, position):
        for i in range(self.nr_hearts):
            current_heart_hp = self.current_hp - i * self.hp_per_heart
            if current_heart_hp >= self.hp_per_heart:
                screen.blit(self.full_heart, (position[0] + self.spacing * i, position[1]))
            elif current_heart_hp > 0:
                screen.blit(self.half_heart, (position[0] + self.spacing * i, position[1]))
            else:
                screen.blit(self.full_heart, (position[0] + self.spacing * i, position[1]))



class BulletIcons():
    def __init__(self, nr_bullets, scale=None):
        self.max_nr_bullets = nr_bullets
        self.nr_bullets = 0
        self.bullet = bullet

        if scale:
            self.bullet = scale_surface_cover(self.bullet, scale)
            self.spacing = scale[0] / 3

    def update(self, level):
        self.mag_ammo = level.equipped_weapon.mag_ammo
        if self.nr_bullets > self.mag_ammo:
            self.nr_bullets = self.mag_ammo
        if self.nr_bullets < self.mag_ammo:
            self.nr_bullets = self.mag_ammo
            if self.nr_bullets > self.max_nr_bullets:
                self.nr_bullets = self.max_nr_bullets

    def draw(self, screen, position):
        for i in range(self.nr_bullets):
            screen.blit(self.bullet, (position[0] + self.spacing * i, position[1]))