import pygame

from button import Button
from player import Player
from gameobject import OnScreen
from block import Block, MovingPlatform, DecayingBlock
from enemy import Enemy, EnemyFlower
from Pickups import Coin, AmmoPickUp, HealthPickUp
from tilemap import TileMap
from mossytile import MossyTile
from scene import Scene
from tunnel import Tunnel

from gun import Pistol

import utils

class Level(OnScreen):
    def __init__(self, screen, level, color):
        self.screen = screen
        self.level = level
        self.color = color
        scene = Scene(screen)
        self.scene = scene

        tunnel_out = Tunnel(pygame.Vector2(700, 200), {}, upwards=False)
        tunnel_in = Tunnel(pygame.Vector2(350, 400), {'tunnel_out':tunnel_out}, upwards=True)

        scene.add_object(tunnel_in)
        scene.add_object(tunnel_out)

        tunnel_out_up = Tunnel(pygame.Vector2(800, 200), {}, upwards=True)
        tunnel_in_up = Tunnel(pygame.Vector2(500, 400), {'tunnel_out':tunnel_out_up}, upwards=True)

        scene.add_object(tunnel_in_up)
        scene.add_object(tunnel_out_up)

        self.weapons = []

        self.initPlayerWithPistol()



        scene.add_object(Block(300, 500, 200, 50))
        scene.add_object(Block(500, 400, 200, 50))
        scene.add_object(Block(200, 400, 200, 50))
        scene.add_object(MovingPlatform(200, 50, pygame.Vector2(100, 200), pygame.Vector2(300, 200), 10))
        # scene.add_object(Enemy(pygame.Vector2(250, 450), pygame.Vector2(350, 450), 2))
        # scene.add_object(EnemyFlower(pygame.Vector2(250, 350), pygame.Vector2(250, 350), 2, self))
        scene.add_object(HealthPickUp(pygame.Vector2(400, 350)))
        scene.add_object(AmmoPickUp(pygame.Vector2(500, 350)))
        scene.add_object(DecayingBlock(150, 150, 1000, 10, 100))
        tilemap = TileMap("assets/tilemaps/level1-map.tmx")
        scene.add_object(tilemap)
        tilemap.create_tiles({'mossy': MossyTile})
        tilemap.create_objects('Objects', {'coin': Coin, 'ammo': AmmoPickUp, 'health': HealthPickUp, 'enemy': Enemy, 'tunnel': Tunnel})

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
