from abc import ABC, abstractmethod
import pymunk

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
