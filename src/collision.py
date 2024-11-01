from enum import Enum

class Layer(Enum):
    PLAYER = 0
    BLOCK = 1

table = {
    (Layer.BLOCK, Layer.PLAYER),
    (Layer.PLAYER, Layer.BLOCK)
}
