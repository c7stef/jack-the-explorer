from gameobject import GameObject
from pytmx import util_pygame
from mossytile import MossyTile

class TileMap(GameObject):
    def __init__(self, tmx_path):
        tmx = util_pygame.load_pygame(tmx_path)
        
        
