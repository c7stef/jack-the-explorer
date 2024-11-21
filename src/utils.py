from enum import Enum
import pygame

import pygame

import Pickups
import enemy
from tunnel import Tunnel

EPSILON = 0.001

escapePressed = False

currentScreen = None
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

importDict = {
    'coin': Pickups.Coin,
    'ammo': Pickups.AmmoPickUp,
    'health': Pickups.HealthPickUp,
    'enemy': enemy.Enemy,
    'tunnel': Tunnel,
    'enemyFlower': enemy.EnemyFlower}

def scale_surface(surface, scale):
    size_x, size_y = surface.get_size()

    original_ratio = size_x / size_y
    new_ratio = scale[0] / scale[1]

    if new_ratio > original_ratio:
        scale_y = scale[1]
        scale_x = scale_y * original_ratio
    else:
        scale_x = scale[0]
        scale_y = scale_x / original_ratio

    return pygame.transform.scale(surface, (scale_x, scale_y))

