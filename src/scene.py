import pygame
import collision
import pymunk
from rigidbody import RigidBody
from pymunk import pygame_util

class Scene:
    def __init__(self, screen):
        self.game_objects = []
        self.physics_space = pymunk.Space()
        self.physics_space.gravity = (0, 4.0)
        self.screen = screen
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

    def remove_object(self, game_object):
        if isinstance(game_object, RigidBody):
            self.physics_space.remove(*game_object.body_data())
        self.game_objects.remove(game_object)

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

    def update(self):
        self.collisions.clear()
        self.physics_space.step(1/4)
        for obj in self.game_objects:
            obj.update()

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for obj in self.game_objects:
            obj.draw(screen)
