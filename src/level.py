import pygame

from player import Player
from gameobject import OnScreen
from block import Block, MovingPlatform, DecayingBlock, Spike
from enemy import Enemy, EnemyFlower
from pickups import Coin, AmmoPickUp, HealthPickUp
from tilemap import TileMap
import mossytile
from mossytile import MossyTile, MossyBgTile
from scene import Scene
from tunnel import TunnelManager
from checkpoint import Checkpoint
from gun import Pistol
from effect import BackgroundTint, BackgroundGradient

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

        scene.add_object(Spike(pygame.Vector2(300, 300), {'width' : 50, 'height' : 50}))
        scene.add_object(Block(300, 500, 200, 50))
        scene.add_object(Block(500, 400, 200, 50))
        scene.add_object(Block(200, 400, 200, 50))
        scene.add_object(Checkpoint(pygame.Vector2(400, 180), {'order': 0}))
        scene.add_object(Checkpoint(pygame.Vector2(600, 180), {'order': 1}))
        scene.add_object(MovingPlatform(200, 50, pygame.Vector2(100, 200), pygame.Vector2(300, 200), 10))
        scene.add_object(Enemy(pygame.Vector2(250, 450), {'xoffset' : 100, 'yoffset' : 0}, 2))
        scene.add_object(EnemyFlower(pygame.Vector2(250, 350), {'xoffset' : 0, 'yoffset' : 0}, 3))
        scene.add_object(HealthPickUp(pygame.Vector2(400, 350)))
        scene.add_object(AmmoPickUp(pygame.Vector2(500, 350)))
        scene.add_object(DecayingBlock(150, 150, 1000, 10, 100))

        self.map_position = pygame.Vector2(-64, -64)

        main_tilemap = TileMap("assets/tilemaps/level1-map.tmx")
        scene.add_object(main_tilemap)

        # Half a tile is cut off on each side
        scene.set_bounds(pygame.Rect(
            pygame.Vector2(0, 0),
            main_tilemap.bounds() - main_tilemap.tile_size()
        ))

        main_tilemap.create_tiles(self.map_position, {'mossy': MossyTile})
        main_tilemap.create_objects(self.map_position, 'Objects', utils.import_dict)

        bg_tilemap = TileMap("assets/tilemaps/level1-bg.tmx")
        scene.add_object(bg_tilemap)

        bg_tilemap.create_tiles(self.map_position, {'mossy': MossyBgTile})

        scene.add_object(BackgroundTint(mossytile.BG_TINT_COLOR))
        scene.add_object(BackgroundGradient(
            mossytile.BG_GRADIENT_COLOR1,
            mossytile.BG_GRADIENT_COLOR2
        ))
        scene.add_object(BackgroundTint((32, 153, 247), z_index=90, alpha=30))

    def update(self):
        self.scene.update()

    def init_player_with_pistol(self):
        self.weapons = []
        self.player = Player(100, 100, self)
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
