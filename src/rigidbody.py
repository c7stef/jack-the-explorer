from abc import ABC, abstractmethod

class RigidBody(ABC):
    @abstractmethod
    def body_data(self):
        raise NotImplementedError("Body data must be specialized by subclasses")