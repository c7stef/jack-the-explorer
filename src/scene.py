import pygame
import collision
import pymunk
from rigidbody import RigidBody
from pymunk import pygame_util

class Scene:
    def __init__(self):
        self.game_objects = []
        self.physics_space = pymunk.Space()
        self.physics_space.gravity = (0, 4.0)

    def add_object(self, game_object):
        game_object.set_scene(self)
        self.game_objects.append(game_object)
        if isinstance(game_object, RigidBody):
            self.physics_space.add(*game_object.body_data())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        self.physics_space.step(1/4)
        for obj in self.game_objects:
            obj.update()

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for obj in self.game_objects:
            obj.draw(screen)

    # def get_collisions(self, object):
    #     collisions = set()
    #     for other in self.game_objects:
    #         if other is object:
    #             continue

    #         collision_pair = (object.layer, other.layer)
    #         if collision_pair in collision.table and other.collides_with(object):
    #             collisions.add(other)

    #     return collisions
