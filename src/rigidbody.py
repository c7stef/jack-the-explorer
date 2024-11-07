from abc import ABC, abstractmethod
import pymunk

class RigidBody(ABC):
    @abstractmethod
    def body_data(self):
        raise NotImplementedError("Body data must be specialized by subclasses")

    def get_collisions(self):
        collisions = []

        def arbiter_check(arbiter):
            n = -arbiter.contact_point_set.normal
            collisions.append({
                "normal": n,
                "penetration": -arbiter.contact_point_set.points[0].distance,
                "shape": arbiter.shapes[1],
                "impulse": arbiter.total_impulse,
                "position": arbiter.contact_point_set.points[0].point_b
            })

        body = [data for data in self.body_data() if isinstance(data, pymunk.Body)][0]
        body.each_arbiter(arbiter_check)

        return collisions