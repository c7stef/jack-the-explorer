from gameobject import GameObject, Solid
from pytmx import util_pygame
import pygame
import pymunk

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
            
            if tile_properties is None:
                raise KeyError(f'Tile with gid={gid} has no properties.')

            if not tile_properties or 'type' not in tile_properties:
                raise KeyError(f'Tile with gid={gid} has no type.')

            tile_type = tile_properties['type']

            if tile_type not in tile_objects_by_type:
                raise KeyError(f'No game object is bound to the tile type {tile_type}')

            tile_image = self.tmx.get_tile_image_by_gid(gid)
            tile_size = self.tile_size().x
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

class SolidTile(Solid):
    def __init__(self, position, image, colliders, layer):
        self.CORNER_RADIUS = 5
        self.z_index = 1
        self.image = image
        
        width, height = self.image.get_width(), self.image.get_height()
        shapes = self.colliders_to_shapes(colliders)
        
        super().__init__(
            position.x, position.y,
            width, height,
            layer=layer,
            shapes=shapes
        )

        for shape in self.shapes:
            shape.body = self.body
    
    def colliders_to_shapes(self, colliders):
        shapes = []

        width, height = self.image.get_width(), self.image.get_height()

        if colliders == []:
            shapes.append(pymunk.Poly.create_box(None, (56, 56), radius=self.CORNER_RADIUS))
        else:
            for poly in colliders:
                points = [(x - width/2, y - height/2) for x, y in poly.apply_transformations()]
                points = [(x * 0.85, y * 0.85) for x, y in points]
                
                shapes.append(pymunk.Poly(None, points, radius=self.CORNER_RADIUS))
        
        return shapes


    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.scene.relative_position((self.body.position.x - self.width / 2, self.body.position.y - self.height / 2)))

class RectangularTile(SolidTile):
    def __init__(self, position, image, colliders, layer):
        super().__init__(position, image, colliders, layer)
    
    def colliders_to_shapes(self, colliders):
        self.CORNER_RADIUS = 10
        shapes = []

        width, height = self.image.get_width(), self.image.get_height()

        for box in colliders:
            points = [(p.x - width/2, p.y - height/2) for p in box.as_points]

            # Manually offset rectangle points
            points[0] = points[0][0] + self.CORNER_RADIUS, points[0][1] + self.CORNER_RADIUS            
            points[1] = points[1][0] + self.CORNER_RADIUS, points[1][1] - self.CORNER_RADIUS
            points[2] = points[2][0] - self.CORNER_RADIUS, points[2][1] - self.CORNER_RADIUS
            points[3] = points[3][0] - self.CORNER_RADIUS, points[3][1] + self.CORNER_RADIUS
            
            shapes.append(pymunk.Poly(None, points, radius=self.CORNER_RADIUS))

        return shapes


class BgTile(GameObject):
    def __init__(self, position, image, colliders):
        self.z_index = -10

        self.position = position
        self.width, self.height = image.get_width(), image.get_height()
        self.image = image

    def update(self):
        pass

    def draw(self, screen):
        position = self.position - pygame.Vector2(self.width, self.height) / 2
        map_size = self.parent.bounds() - self.parent.tile_size()
        screen.blit(self.image, self.scene.relative_position_parallax(position, map_size))

