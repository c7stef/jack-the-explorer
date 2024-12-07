from enum import Enum
import pygame

import block
import pickups
import enemy
from checkpoint import Checkpoint
from tunnel import Tunnel

EPSILON = 0.001

escape_pressed = False

current_screen = None

controls = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'sound': 0.5,
    'resolution': "1600x1000"
}

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

import_dict = {
    'coin': pickups.Coin,
    'ammo': pickups.AmmoPickUp,
    'health': pickups.HealthPickUp,
    'enemy': enemy.Enemy,
    'tunnel': Tunnel,
    'checkpoint': Checkpoint,
    'spike': block.Spike,
    'enemy_flower': enemy.EnemyFlower
}



