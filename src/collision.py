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
    (Layer.PLAYER, Layer.BLOCK),
    (Layer.PLAYER, Layer.PLATFORM),
    (Layer.PLAYER, Layer.ENEMY),
    (Layer.PLAYER, Layer.COIN),
    (Layer.PLAYER, Layer.DECBLOCK),
    (Layer.BULLET, Layer.BLOCK),
    (Layer.BULLET, Layer.ENEMY)
}
