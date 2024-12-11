import pygame
import pymunk

from collision import Layer
import utils
from gameobject import Solid, Named

from image_processing import scale_surface
from animated_sprite import AnimatedSprite

flag_white = AnimatedSprite("assets/checkpoint/white", (54, 80), 8)
flag_green = AnimatedSprite("assets/checkpoint/green", (54, 80), 8)
checkpoint_sound = pygame.mixer.Sound("sounds/checkpoint.mp3")

class Checkpoint(Solid, Named):
    def __init__(self, position, properties=None):
        super().__init__(position.x, position.y, 50, 50,
        body_type=pymunk.Body.STATIC, layer=Layer.CHECKPOINT.value)
        self.shape.sensor = True

        self.order = properties.get('order', 0)
        self.player = None

        self.current_sprite = flag_white

    def update(self):
        if self.player and self.player.last_checkpoint is not self:
            self.current_sprite = flag_white
        self.current_sprite.update()

    def draw(self, screen):
        self.current_sprite.draw(screen, self.scene.relative_position(self.body.position))

    def reached(self, player):
        self.player = player
        if self.player.last_checkpoint is not self:
            checkpoint_sound.play()
            checkpoint_sound.set_volume(utils.controls['sound'])
            self.current_sprite = flag_green
            player.last_checkpoint = self
            return self
        return self

    def reset(self):
        self.current_sprite = flag_white

    @property
    def name(self):
        return "Checkpoint"
