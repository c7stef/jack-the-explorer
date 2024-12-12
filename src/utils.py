from enum import Enum
import pygame

import enemy
import pickups
import enemy
from checkpoint import Checkpoint
from tunnel import Tunnel
import block

EPSILON = 0.001

escape_pressed = False

current_screen = None

pygame.font.init()
ui_font = pygame.font.Font('assets/fonts/Chewy-Regular.ttf', 52)

controls = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s,
    'sound': 0.5,
    'reload': pygame.K_r,
    'resolution': "1440x900",
    'fullscreen': False
}

music_being_played = None

def play_music(music):
    global music_being_played
    if music is None:
        if music_being_played is not None:
            pygame.mixer.music.stop()
            music_being_played = None
        return
    if music_being_played == music:
        return
    if music_being_played is not None:
        pygame.mixer.music.stop()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(controls['sound'] / 2)
    music_being_played = music

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

level1_objects = {
    'coin': pickups.Coin,
    'ammo': pickups.AmmoPickUp,
    'health': pickups.HealthPickUp,
    'enemy': enemy.Enemy,
    'tunnel': Tunnel,
    'checkpoint': Checkpoint,
    'spike': enemy.Spike,
    'enemy_flower': enemy.EnemyFlower,
    'moving_platform': block.MovingPlatform,
}

