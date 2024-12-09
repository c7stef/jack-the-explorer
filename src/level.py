import pygame

from player import Player
from gameobject import OnScreen
from tilemap import TileMap
import mossytile
from mossytile import MossyTile, MossyBgTile
from scene import Scene
from tunnel import TunnelManager
from gun import Pistol
from effect import TintEffect, BackgroundGradient, BackgroundParticles
from scifi_tile import SciFiTile

import utils

class Level(OnScreen):
    def __init__(self, level_menu, level, color):
        self.level_menu = level_menu
        self.screen = level_menu.screen
        self.num_level = level
        self.color = color
        scene = Scene(self.screen)
        self.scene = scene

        scene.add_object(TunnelManager())

        self.weapons = []

        self.init_player_with_pistol()

        self.map_position = pygame.Vector2(-64, -64)

        # main_tilemap = TileMap("assets/sci-fi-tilemap/sci-fi-map.tmx")
        main_tilemap = TileMap("assets/mossy-tilemap/level1-map.tmx")
        scene.add_object(main_tilemap)

        # Half a tile is cut off on each side
        scene.set_bounds(pygame.Rect(
            pygame.Vector2(0, 0),
            main_tilemap.bounds() - main_tilemap.tile_size()
        ))

        main_tilemap.create_tiles(self.map_position, {'mossy': MossyTile, 'scifi_tile': SciFiTile})
        main_tilemap.create_objects(self.map_position, 'Objects', utils.level1_objects)

        bg_tilemap = TileMap("assets/mossy-tilemap/level1-bg.tmx")
        scene.add_object(bg_tilemap)

        bg_tilemap.create_tiles(self.map_position, {'mossy': MossyBgTile})

        scene.add_object(TintEffect(mossytile.BG_TINT_COLOR))
        scene.add_object(BackgroundGradient(
            mossytile.BG_GRADIENT_COLOR1,
            mossytile.BG_GRADIENT_COLOR2
        ))
        scene.add_object(TintEffect(mossytile.FG_TINT_COLOR, z_index=90, alpha=30))

        scene.add_object

    def update(self):
        self.scene.update()

    def init_player_with_pistol(self):
        self.weapons = []
        self.player = Player(832, 1128, self)
        # self.player = Player(512, 1016, self)
        self.scene.following = self.player
        gun = Pistol(self)
        self.weapons.append(gun)
        self.player.equip_weapon(gun)
        self.scene.add_object(self.player)
        self.scene.add_object(gun)

        self.scene.add_object(BackgroundParticles())

        self.score = 0
        self.coin_cnt = 0
        self.current_ammo = 0

        self.hp = 10
        self.max_hp = 10

        self.equipped_weapon = self.weapons[0]
        self.equipped_weapon.equip()


    def draw(self):
        self.scene.draw(self.screen)
