from abc import ABC, abstractmethod
import pymunk
import pygame
import collision

from image_processing import scale_surface

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

    @property
    def z_index(self):
        if not hasattr(self, '_z_index'):
            self._z_index = 0
        return self._z_index

    @z_index.setter
    def z_index(self, value):
        self._z_index = value

    @abstractmethod
    def update(self):
        raise NotImplementedError("Update method must be implemented by subclasses")

    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError("Draw method must be implemented by subclasses")

class OnScreen(ABC):
    def set_screen_size(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.button_width = self.screen_width / 5
        self.button_height = self.screen_height / 9
        self.offset = self.screen_height / 18
        self.center_button_x = self.screen_width / 2 - self.button_width / 2
        self.center_button_y = self.screen_height / 2 - self.button_height / 2
        self.font_ratio = 0.04
        self.font_size = int(self.screen_height * self.font_ratio)

    def set_screen(self, screen):
        self.screen = screen

    def send_events(self, events):
        self.events = events

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

class Followable(ABC):
    @property
    @abstractmethod
    def position(self):
        raise NotImplementedError("Position must be specialized by subclasses")

class Named(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError("Name must be specialized by subclasses")

class Solid(GameObject, RigidBody):
    def __init__(self, x, y, width, height, body_type=pymunk.Body.STATIC, shapes=None, layer=collision.Layer.BLOCK.value):
        moment = pymunk.moment_for_box(mass=10, size=(width, height))
        self.body = pymunk.Body(mass=10, moment=moment, body_type=body_type)
        self.body.position = (x, y)

        self.shapes = shapes if shapes else [
            pymunk.Poly.create_box(self.body, size=(width, height))
        ]

        for shape in self.shapes:
            shape.collision_type = layer

        self.width = width
        self.height = height

    def body_data(self):
        return (self.body, *self.shapes)

    @property
    def shape(self):
        if not self.shapes:
            raise AttributeError("No shapes in solid")
        if len(self.shapes) > 1:
            raise AttributeError("Solid has multiple shapes")
        return self.shapes[0]

    def update(self):
        pass

    def draw(self, screen):
        pass

class ImageObject(GameObject):
    def __init__(self, rect, width, height, image):
        self.image = image
        self.image['default'] = scale_surface(self.image['default'], (width, height))
        self.image['hover'] = scale_surface(self.image['hover'], (width, height))
        self.rect = rect
        self.hover = False

    def update(self):
        pass

    def draw(self, screen):
        if self.hover:
            screen.blit(self.image['hover'], pygame.Vector2(self.rect.center) - pygame.Vector2(self.image['hover'].get_size()) / 2)
        else:
            screen.blit(self.image['default'], pygame.Vector2(self.rect.center) - pygame.Vector2(self.image['default'].get_size()) / 2)