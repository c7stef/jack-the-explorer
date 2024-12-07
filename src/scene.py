import pygame
import pymunk

from gameobject import RigidBody, Named
from pymunk import pygame_util
from camera import Camera
from player import Player
import collision
from sortedcontainers import SortedList

class Scene:
    def __init__(self, screen):
        self.game_objects = SortedList(key=lambda x: x.z_index)
        self.physics_space = pymunk.Space()
        self.physics_space.gravity = (0, 4.0)
        self.following = None
        self.screen = screen
        self.to_remove = []

        camera_rect = screen.get_rect()
        self.camera = Camera(self.update_camera, camera_rect.center, camera_rect.w, camera_rect.h)

        self.collisions = []

        for type_a, type_b in collision.table:
            def pre_solve_collision(arbiter, space, data):
                self.collisions.append((
                    arbiter.shapes,
                    {
                        "normal": -arbiter.contact_point_set.normal
                    }
                ))
                return True
            handler = self.physics_space.add_collision_handler(type_a.value, type_b.value)
            handler.pre_solve = pre_solve_collision

    def set_bounds(self, bounds):
        self.map_bounds = bounds

    def add_object(self, game_object):
        game_object.set_scene(self)
        self.game_objects.add(game_object)
        if isinstance(game_object, RigidBody):
            self.physics_space.add(*game_object.body_data())
        if isinstance(game_object, Player):
            self.camera.following = game_object

    def remove_object(self, game_object):
        # Remove children first
        for other in self.game_objects:
            if other.parent == game_object:
                self.remove_object(other)

        # Add to delete list
        self.to_remove.append(game_object)

    def collect_garbage(self):
        for game_object in self.to_remove:
            # Remove from physics space
            if isinstance(game_object, RigidBody):
                self.physics_space.remove(*game_object.body_data())

            # Remove from scene
            self.game_objects.remove(game_object)

        # Clear delete list
        self.to_remove.clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def find_rigid_body(self, shape):
        for obj in self.game_objects:
            if isinstance(obj, RigidBody) and shape in obj.body_data():
                return obj
        return None

    def find_player(self):
        for obj in self.game_objects:
            if isinstance(obj, Player):
                return obj
        return None
    
    def find_objects_by_name(self, name):
        return [obj for obj in self.game_objects if isinstance(obj, Named) and obj.name == name]
    
    def find_object_by_name(self, name):
        objects = self.find_objects_by_name(name)
        if len(objects) != 1:
            return None
        return objects[0]

    def update(self):
        self.collisions.clear()
        self.physics_space.step(6/20)
        for obj in self.game_objects:
            obj.update()
        self.camera.update()
        self.collect_garbage()

    def update_camera(self):
        camera_rect = self.camera.rect

        player_pos = self.following.position

        left_limit = self.map_bounds.left
        right_limit = self.map_bounds.right
        top_limit = self.map_bounds.top
        bottom_limit = self.map_bounds.bottom

        if player_pos.x <= left_limit + camera_rect.width / 2:
            player_pos.x = left_limit + camera_rect.width / 2
        
        if player_pos.x >= right_limit - camera_rect.width / 2:
            player_pos.x = right_limit - camera_rect.width / 2

        if player_pos.y <= top_limit + camera_rect.height / 2:
            player_pos.y = top_limit + camera_rect.height / 2

        if player_pos.y >= bottom_limit - camera_rect.height / 2:
            player_pos.y = bottom_limit - camera_rect.height / 2

        return player_pos

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for obj in self.game_objects:
            obj.draw(screen)
    def relative_position_parallax(self, position, size):
        camera_size = pygame.Vector2(self.camera.rect.size)
        main_size = pygame.Vector2(self.map_bounds.size)
        
        parallax_gap = main_size - size
        camera_gap = main_size - camera_size

        factor = pygame.Vector2(
            parallax_gap.x / camera_gap.x - 1,
            parallax_gap.y / camera_gap.y - 1
        )

        return self.camera.relative_position_scaled(position, factor)

    def relative_position(self, position):
        return self.camera.relative_position(position)

    def relative_rect(self, rect):
        return self.camera.relative_rect(rect)
