import pygame
import pymunk

from gameobject import RigidBody, Named
from pymunk import pygame_util
from camera import Camera
from player import Player
import collision

class Scene:
    def __init__(self, screen):
        self.game_objects = []
        self.physics_space = pymunk.Space()
        self.physics_space.gravity = (0, 4.0)
        self.following = None
        self.screen = screen
        self.to_remove = []

        self.map_bounds = pygame.Rect(0, 0, 2000, 2000)

        def follow_player():
            if not self.following:
                return None
            return self.following.position

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

    def add_object(self, game_object):
        game_object.set_scene(self)
        self.game_objects.append(game_object)
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
        self.camera.update()

        camera_rect = self.camera.rect

        player_pos = self.following.position

        left_limit = self.map_bounds.left
        right_limit = self.map_bounds.right
        top_limit = self.map_bounds.top
        bottom_limit = self.map_bounds.bottom

        fixed_camera_position = camera_rect.center

        if camera_rect.left <= left_limit:
            self.camera.rect.left = left_limit
            fixed_camera_position = (self.camera.rect.centerx, self.camera.rect.centery)
            if player_pos.x > camera_rect.centerx:
                self.camera.rect.centerx = min(player_pos.x, right_limit - camera_rect.width / 2)
        
        if camera_rect.right >= right_limit:
            self.camera.rect.right = right_limit
            fixed_camera_position = (self.camera.rect.centerx, self.camera.rect.centery)
            if player_pos.x < camera_rect.centerx:
                self.camera.rect.centerx = max(player_pos.x, left_limit + camera_rect.width / 2)

        if camera_rect.top <= top_limit:
            self.camera.rect.top = top_limit
            fixed_camera_position = (self.camera.rect.centerx, self.camera.rect.centery)
            if player_pos.y > camera_rect.centery:
                self.camera.rect.centery = min(player_pos.y, bottom_limit - camera_rect.height / 2)

        if camera_rect.bottom >= bottom_limit:
            self.camera.rect.bottom = bottom_limit
            fixed_camera_position = (self.camera.rect.centerx, self.camera.rect.centery)
            if player_pos.y < camera_rect.centery:
                self.camera.rect.centery = max(player_pos.y, top_limit + camera_rect.height / 2)

        if (left_limit <= camera_rect.left and
            camera_rect.right <= right_limit and
            top_limit <= camera_rect.top and
            camera_rect.bottom <= bottom_limit):
            return player_pos
        else:
            return fixed_camera_position

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for obj in self.game_objects:
            obj.draw(screen)

    def relative_position(self, position):
        return self.camera.relative_position(position)

    def relative_rect(self, rect):
        return self.camera.relative_rect(rect)
