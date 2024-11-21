from enum import Enum

EPSILON = 0.001

escapePressed = False

currentScreen = None
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
