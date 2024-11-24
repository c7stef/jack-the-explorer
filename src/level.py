import pygame

from button import Button
from player import Player
from gameobject import OnScreen
from block import Block, MovingPlatform, DecayingBlock, Spike
from enemy import Enemy, EnemyFlower
from Pickups import Coin, AmmoPickUp, HealthPickUp
from tilemap import TileMap
from mossytile import MossyTile
from scene import Scene
from tunnel import Tunnel, TunnelManager

from gun import Pistol

import utils

class Level(OnScreen):
    def __init__(self, screen, level, color):
        self.screen = screen
        self.level = level
        self.color = color
        scene = Scene(screen)
        self.scene = scene

        scene.add_object(TunnelManager())

        self.weapons = []

        self.initPlayerWithPistol()

        scene.add_object(Spike(300, 300, 50, 50))
        scene.add_object(Block(300, 500, 200, 50))
        scene.add_object(Block(500, 400, 200, 50))
        scene.add_object(Block(200, 400, 200, 50))
        scene.add_object(MovingPlatform(200, 50, pygame.Vector2(100, 200), pygame.Vector2(300, 200), 10))
        scene.add_object(Enemy(pygame.Vector2(250, 450), {'xoffset' : 100, 'yoffset' : 0}, 2))
        scene.add_object(EnemyFlower(pygame.Vector2(250, 350), {'xoffset' : 0, 'yoffset' : 0}, 3))
        scene.add_object(HealthPickUp(pygame.Vector2(400, 350)))
        scene.add_object(AmmoPickUp(pygame.Vector2(500, 350)))
        scene.add_object(DecayingBlock(150, 150, 1000, 10, 100))
        tilemap = TileMap("assets/tilemaps/level1-map.tmx")
        scene.add_object(tilemap)
        tilemap.create_tiles({'mossy': MossyTile})
        tilemap.create_objects('Objects', utils.importDict)

    def update(self):
        self.scene.update()

    def initPlayerWithPistol(self):
        self.weapons = []
        self.player = Player(100, 100, self)
        self.scene.following = self.player
        gun = Pistol(self)
        self.weapons.append(gun)
        self.player.equipWeapon(gun)
        self.scene.add_object(self.player)
        self.scene.add_object(gun)

        self.score = 0
        self.coinCnt = 0
        self.currentAmmo = 0

        self.hp = 10
        self.maxHp = 10

        self.equippedWeapon = self.weapons[0]
        self.equippedWeapon.equip()


    def draw(self):
        self.scene.draw(self.screen)
