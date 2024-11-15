from abc import ABC, abstractmethod
import pymunk
import pygame

class GameObject(ABC):
    def set_scene(self, scene):
        self.scene = scene

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)

    @property
    def parent(self):
        if not hasattr(self, '_parent'):
            self._parent = None
        return self._parent

    @parent.setter
    def parent(self, game_object):
        self._parent = game_object

    @abstractmethod
    def update(self):
        raise NotImplementedError("Update method must be implemented by subclasses")

    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError("Draw method must be implemented by subclasses")

class OnScreen(ABC):
    def setScreen(self, screen):
        self.screen = screen

    @abstractmethod
    def update(self):
        raise NotImplementedError("Update method must be implemented by subclasses")

    @abstractmethod
    def draw(self):
        raise NotImplementedError("Draw method must be implemented by subclasses")


class RigidBody(ABC):
    @abstractmethod
    def body_data(self):
        raise NotImplementedError("Body data must be specialized by subclasses")

    def get_collisions(self):
        collisions = self.scene.collisions

        own_shape = [data for data in self.body_data() if isinstance(data, pymunk.Shape)][0]
        return [{
            "normal": data["normal"],
            "shape": pair[0] if pair[1] == own_shape else pair[1]
        } for pair, data in collisions if own_shape in pair]


class Solid(GameObject, RigidBody):
    def __init__(self, x, y, width, height, body_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.position = pygame.Vector2(x, y)

        self.moment = pymunk.moment_for_box(mass=10, size=(width, height))
        self.body = pymunk.Body(mass=10, moment=self.moment, body_type=body_type)
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, size=(width, height))

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def body_data(self):
        return (self.body, self.shape)

    def update(self):
        pass

    def draw(self, screen):
        pass

