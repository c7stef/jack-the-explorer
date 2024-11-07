from enum import Enum

class Layer(Enum):
    PLAYER = 1
    BLOCK = 2

table = {
    (Layer.BLOCK, Layer.PLAYER),
    (Layer.PLAYER, Layer.BLOCK)
}
