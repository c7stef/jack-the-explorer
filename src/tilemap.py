from gameobject import GameObject
from pytmx import util_pygame
import pygame

class TileMap(GameObject):
    def __init__(self, tmx_path):
        self.tmx = util_pygame.load_pygame(tmx_path)

    def create_objects(self, position, layer, objects_by_type):
        objects_layer = self.tmx.get_layer_by_name(layer)

        for obj in objects_layer:
            if obj.type not in objects_by_type:
                raise KeyError(f'No game object is bound to the object name {obj.name}, type {obj.type}')

            obj_class = objects_by_type[obj.type]

            obj_size = pygame.Vector2(obj.width, obj.height)
            obj_centre = position + pygame.Vector2(obj.x, obj.y) + obj_size/2

            game_object = obj_class(obj_centre, obj.properties)
            game_object.parent = self

            self.scene.add_object(game_object)

    def create_tiles(self, position, tile_objects_by_type):
        tile_colliders_by_gid = {
            gid: colliders for gid, colliders in self.tmx.get_tile_colliders()
        }

        platform_layer = self.tmx.get_layer_by_name("Platform")

        for column, row, gid in platform_layer.iter_data():
            if gid == 0:
                continue

            tile_properties = self.tmx.get_tile_properties_by_gid(gid)

            if 'type' not in tile_properties:
                raise KeyError(f'Tile with gid={gid} has no type.')

            tile_type = tile_properties['type']

            if tile_type not in tile_objects_by_type:
                raise KeyError(f'No game object is bound to the tile type {tile_type}')

            tile_image = self.tmx.get_tile_image_by_gid(gid)
            tile_size = self.tmx.tilewidth
            tile_position = position + pygame.Vector2(column, row) * tile_size
            tile_colliders = tile_colliders_by_gid.get(gid, [])
            tile_centre = tile_position + pygame.Vector2(tile_size, tile_size) / 2

            tile = tile_objects_by_type[tile_type](tile_centre, tile_image, tile_colliders)
            tile.parent = self

            self.scene.add_object(tile)
    
    def bounds(self):
        return pygame.Vector2(
            self.tmx.width * self.tmx.tilewidth,
            self.tmx.height * self.tmx.tileheight
        )

    def tile_size(self):
        return pygame.Vector2(self.tmx.tilewidth, self.tmx.tileheight)

    def update(self):
        pass

    def draw(self, screen):
        pass
