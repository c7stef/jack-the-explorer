from enum import Enum
import pygame

import block
import Pickups
import enemy
from checkpoint import Checkpoint
from tunnel import Tunnel

EPSILON = 0.001

escapePressed = False

currentScreen = None

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

importDict = {
    'coin': Pickups.Coin,
    'ammo': Pickups.AmmoPickUp,
    'health': Pickups.HealthPickUp,
    'enemy': enemy.Enemy,
    'tunnel': Tunnel,
    'checkpoint': Checkpoint,
    'spike': block.Spike,
    'enemyFlower': enemy.EnemyFlower}



