from abc import ABC, abstractmethod

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
