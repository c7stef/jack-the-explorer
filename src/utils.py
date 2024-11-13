from enum import Enum

EPSILON = 0.001

scene = None
player = None
maxAmmo = 100
currentAmmo = 10
score = 0
coinCnt = 0
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
