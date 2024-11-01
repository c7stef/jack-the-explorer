import pygame
import collision

class Scene:
    def __init__(self):
        self.game_objects = []

    def add_object(self, game_object):
        game_object.set_scene(self)
        self.game_objects.append(game_object)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        for obj in self.game_objects:
            obj.update()

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for obj in self.game_objects:
            obj.draw(screen)

    def get_collisions(self, object):
        collisions = set()
        for other in self.game_objects:
            if other is object:
                continue

            collision_pair = (object.layer, other.layer)
            if collision_pair in collision.table and other.collides_with(object):
                collisions.add(other)
        
        return collisions
