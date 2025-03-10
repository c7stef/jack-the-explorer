import pygame

from player import Player
from gameobject import OnScreen
from tilemap import TileMap, BgTile
import mossytile
from mossytile import MossyTile
from scene import Scene
from tunnel import TunnelManager
from gun import Pistol
from effect import TintEffect, BackgroundGradient, BackgroundParticles, BgImage
import scifi_tile
from scifi_tile import SciFiTile
from enemy import SpikeTile
import winter
from winter import WinterTile

import utils

class LevelData:
    def __init__(self, player_pos, tilemap_path, bg_path,
                 tile_objects_by_type=None, bg_tile_objects_by_type=None,
                 bg_image=None,
                 effects=[], background_music=None):
        self.player_pos = player_pos
        self.tilemap_path = tilemap_path
        self.bg_path = bg_path
        self.tile_objects_by_type = tile_objects_by_type
        self.bg_tile_objects_by_type = bg_tile_objects_by_type
        self.effects = effects
        self.background_music = background_music
        self.bg_image = bg_image

level_data = {
    1: LevelData(
        player_pos=(832, 1128),
        tilemap_path="assets/mossy-tilemap/level1-map.tmx",
        bg_path="assets/mossy-tilemap/level1-bg.tmx",
        tile_objects_by_type={'mossy': MossyTile},
        bg_tile_objects_by_type={'mossy': BgTile},
        effects=[
            TintEffect(mossytile.BG_TINT_COLOR),
            BackgroundGradient(mossytile.BG_GRADIENT_COLOR1,
                mossytile.BG_GRADIENT_COLOR2),
            TintEffect(mossytile.FG_TINT_COLOR, z_index=90, alpha=30),
            BackgroundParticles()
        ],
        background_music="sounds/music/lv1.mp3"

    ),
    2: LevelData(
        player_pos=(256, 508),
        tilemap_path="assets/sci-fi-tilemap/level2-map.tmx",
        bg_path="assets/sci-fi-tilemap/level2-bg.tmx",
        tile_objects_by_type={'scifi_tile': SciFiTile, 'spike': SpikeTile},
        bg_image="assets/sci-fi-tilemap/level2-bg.png",
        effects=[
            TintEffect(scifi_tile.BG_TINT_COLOR, alpha=180),
            BackgroundGradient(scifi_tile.BG_GRADIENT_COLOR1, scifi_tile.BG_GRADIENT_COLOR2),
            TintEffect(scifi_tile.FG_TINT_COLOR, z_index=90, alpha=40)
        ],
        background_music="sounds/music/lv2.mp3"
    ),
    3: LevelData(
        player_pos=(256, 508),
        tilemap_path="assets/winter-tilemap/level3.tmx",
        bg_path="assets/winter-tilemap/level3-bg.tmx",
        tile_objects_by_type={'winter_tile' : WinterTile, 'spike': SpikeTile},
        bg_tile_objects_by_type={'winter_tile' : BgTile, 'mossy': BgTile},
        effects=[
            TintEffect(winter.BG_TINT_COLOR, alpha=180),
            BackgroundGradient(winter.BG_GRADIENT_COLOR1, winter.BG_GRADIENT_COLOR2),
            TintEffect(winter.FG_TINT_COLOR, z_index=90, alpha=40)
        ],
        background_music="sounds/music/lv3.mp3"
    )
}

class Level(OnScreen):
    def __init__(self, level_menu, level):
        self.level_menu = level_menu
        self.screen = level_menu.screen
        self.num_level = level
        scene = Scene(self.screen)
        self.scene = scene

        scene.add_object(TunnelManager())

        self.weapons = []

        self.init_player_with_pistol()

        main_tilemap = TileMap(level_data[self.num_level].tilemap_path)
        self.map_position = -main_tilemap.tile_size() / 2
        scene.add_object(main_tilemap)

        # Half a tile is cut off on each side
        scene.set_bounds(pygame.Rect(
            pygame.Vector2(0, 0),
            main_tilemap.bounds() - main_tilemap.tile_size()
        ))

        main_tilemap.create_tiles(self.map_position, level_data[self.num_level].tile_objects_by_type)
        main_tilemap.create_objects(self.map_position, 'Objects', utils.level1_objects)

        bg_tilemap = TileMap(level_data[self.num_level].bg_path)
        scene.add_object(bg_tilemap)

        if level_data[self.num_level].bg_tile_objects_by_type:
            bg_tilemap.create_tiles(self.map_position, level_data[self.num_level].bg_tile_objects_by_type)

        if level_data[self.num_level].bg_image:
            scene.add_object(BgImage(level_data[self.num_level].bg_image, main_tilemap.tile_size()))

        for effect in level_data[self.num_level].effects:
            scene.add_object(effect)
        
    def update(self):
        self.scene.update()

    def init_player_with_pistol(self):
        utils.play_music(level_data[self.num_level].background_music)
        self.weapons = []
        self.player = Player(*level_data[self.num_level].player_pos, self)
        self.scene.following = self.player
        gun = Pistol(self)
        self.weapons.append(gun)
        self.player.equip_weapon(gun)
        self.scene.add_object(self.player)
        self.scene.add_object(gun)

        self.score = 0
        self.coin_cnt = 0
        self.current_ammo = 0

        self.hp = 10
        self.max_hp = 10

        self.equipped_weapon = self.weapons[0]
        self.equipped_weapon.equip()


    def draw(self):
        self.scene.draw(self.screen)
