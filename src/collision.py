from enum import Enum

class Layer(Enum):
    PLAYER = 1
    BLOCK = 2
    PLATFORM = 3
    ENEMY = 4
    COIN = 5
    BULLET = 6
    DECBLOCK = 7

COLLISION_DISABLED = 1

table = {
    (Layer.BLOCK, Layer.PLAYER),
    (Layer.PLAYER, Layer.BLOCK)
}
