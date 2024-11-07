import pygame
import collision
from gameobject import GameObject
import pymunk
from rigidbody import RigidBody

# Player class
class Player(GameObject, RigidBody):
    def __init__(self, x, y):
        self.JUMP_STRENGTH = -300
        self.MOVE_STRENGTH = 150
        self.MAX_VELOCITY = 30
        
        self.layer = collision.Layer.PLAYER

        self.moment = pymunk.moment_for_box(mass=10, size=(50, 50))
        self.body = pymunk.Body(mass=10, moment=float("inf"))
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, size=(50, 50))
        self.shape.friction = 0
        self.shape.collision_type = collision.Layer.PLAYER.value
        
        self.width = 50
        self.height = 50
        
        self.is_on_ground = False
    
    def body_data(self):
        return (self.body, self.shape)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.body.apply_impulse_at_local_point((-self.MOVE_STRENGTH, 0))
        elif keys[pygame.K_RIGHT]:
            self.body.apply_impulse_at_local_point((self.MOVE_STRENGTH, 0))

        if keys[pygame.K_SPACE] and self.is_on_ground:
            self.body.apply_impulse_at_local_point((0, self.JUMP_STRENGTH))

    def update(self):
        self.body.velocity = 0, self.body.velocity.y

        grounding = {
            "normal": pygame.Vector2(),
            "penetration": pygame.Vector2(),
            "impulse": pygame.Vector2(),
            "position": pygame.Vector2(),
            "body": None,
        }

        # Check if player is standing on ground
        def arbiter_check(arbiter):
            n = -arbiter.contact_point_set.normal
            if n.y < grounding["normal"].y:
                grounding["normal"] = n
                grounding["penetration"] = -arbiter.contact_point_set.points[0].distance
                grounding["body"] = arbiter.shapes[1].body
                grounding["impulse"] = arbiter.total_impulse
                grounding["position"] = arbiter.contact_point_set.points[0].point_b

        self.body.each_arbiter(arbiter_check)

        self.is_on_ground = False
        if grounding["body"] != None:
            self.is_on_ground = True

        self.handle_input()

        if self.body.velocity.y < -self.MAX_VELOCITY:
            self.body.velocity = self.body.velocity.x, -self.MAX_VELOCITY

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2, self.width, self.height))

