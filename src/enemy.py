import pygame
import pymunk
import particlepy
import random

from gameobject import Solid, GameObject
from tilemap import SolidTile
from bullet import EnemyBullet
import collision
import utils
from animated_sprite import AnimatedSprite
from image_processing import scale_surface_contain

def load_sprite(path):
    return scale_surface_contain(
        pygame.image.load(path),
        (50, 50),
    )

flower_sprite = load_sprite("assets/enemy/skull/idle.png")
flower_hit_sprite = load_sprite("assets/enemy/skull/hit.png")
spike_wood_sprite = load_sprite("assets/spike/spike_wood.png")

enemy_shooting_sound = pygame.mixer.Sound("sounds/enemy_shooting.mp3")

class Enemy(Solid):
    def __init__(self, position, properties, custom_sprite=None, hit_sprite=None):
        super().__init__(position.x, position.y, 54, 54,
                         body_type=pymunk.Body.KINEMATIC,
                         layer=collision.Layer.ENEMY.value)
        health = properties.get('health', 3)
        self.p1 = position
        xoffset = properties.get('xoffset', 0)
        yoffset = properties.get('yoffset', 0)
        self.HIT_EFFECT_TIME = 22
        self.hit_timer = 0
        self.p2 = position + pygame.Vector2(xoffset, yoffset)
        self.t = 0
        distance_to_move = (self.p2 - self.p1).magnitude()
        if distance_to_move > utils.EPSILON:
            self.dt = 1 / distance_to_move
        else:
            self.dt = 0

        self.shape.filter = pymunk.ShapeFilter(categories=collision.Layer.ENEMY.value, mask=collision.Layer.BLOCK.value | collision.Layer.PLATFORM.value)

        self.hp = health
        self.max_health = health

        if custom_sprite is not None:
            self.sprite = custom_sprite
            self.current_sprite = custom_sprite
            self.hit_sprite = hit_sprite
        else:
            self.sprite = AnimatedSprite("assets/enemy/bug", (60, 60), 5)
            self.sprite_flipped = self.sprite.flipped()

            self.current_sprite = self.sprite

    def update(self):
        self.t += self.dt
        if self.t > 1:
            self.dt = -self.dt
            self.t = 1
        if self.t < 0:
            self.dt = -self.dt
            self.t = 0
        # lerp is linear interpolation
        self.body.position = tuple(self.p1.lerp(self.p2, self.t))

        if self.hit_timer == 0:
            if isinstance(self.current_sprite, AnimatedSprite):
                self.current_sprite = self.sprite if self.dt > 0 else self.sprite_flipped
                self.current_sprite.update()
            else:
                self.current_sprite = self.sprite
            self.current_sprite.set_alpha(255)

        if self.hit_timer > 0:
            self.hit_timer -= 1
            if hasattr(self, 'hit_sprite'):
                self.current_sprite = self.hit_sprite
            self.current_sprite.set_alpha(20 if self.hit_timer % 6 < 3 else 255)

    def deal_damage(self, damage):
        self.hp -= damage
        if hasattr(self, 'hit_sprite'):
            self.current_sprite = self.hit_sprite
        if self.hp <= 0:
            self.scene.remove_object(self)
        self.hit_timer = self.HIT_EFFECT_TIME

    def draw(self, screen):
        if isinstance(self.current_sprite, AnimatedSprite):
            self.current_sprite.draw(screen, self.scene.relative_position(pygame.Vector2(self.body.position)))
        else:
            screen.blit(
                self.current_sprite,
                self.scene.relative_position(
                    pygame.Vector2(self.body.position)
                        - pygame.Vector2(self.current_sprite.get_size()) / 2
                )
            )

class FlowerFire(GameObject):
    def __init__(self, position):
        self.z_index = -1
        self.position = position
        self.particle_system = particlepy.particle.ParticleSystem()
        self.relative_position = self.position
        self.alive = True
        self.death_timer = 0
        self.DEATH_REMOVE_TIME = 300

    def position_range(self):
        def value_range(value):
            return random.uniform(value - 20, value + 20)
        return value_range(self.relative_position.x), value_range(self.relative_position.y)

    def stop(self):
        self.alive = False
        self.death_timer = self.DEATH_REMOVE_TIME

    def update(self):
        self.particle_system.update(1/120)

        if self.alive:
            for _ in range(6):
                self.particle_system.emit(
                    particlepy.particle.Particle(
                        shape=particlepy.shape.Circle(
                            radius=random.randint(5, 10),
                            color=(250, random.randint(100, 200), 50),
                            alpha=130),
                        position=self.position_range(),
                        velocity=(random.uniform(-50, 50), random.uniform(-300, -150)),
                        delta_radius=0.2))

        else:
            self.death_timer -= 1
            if self.death_timer == 0:
                self.scene.remove_object(self)

        # color manipulation
        for particle in self.particle_system.particles:
            # particle.shape.color = particlepy.math.fade_color(
            #     particle=particle,
            #     color=,
            #     progress=particle.inverted_progress)
            particle.shape.alpha = particlepy.math.fade_alpha(particle, 0, progress=particle.inverted_progress)

        # render shapes
        self.particle_system.make_shape()

        for particle in self.particle_system.particles:
            particle.position += self.scene.relative_position(self.position) - self.relative_position

        self.relative_position = self.scene.relative_position(self.position)

    def draw(self, screen):
        self.particle_system.render(surface=screen)

class EnemyFlower(Enemy):
    def __init__(self, position, properties):
        super().__init__(
            position, properties,
            custom_sprite=flower_sprite,
            hit_sprite=flower_hit_sprite
        )
        self.color = (250, 40, 60)
        self.fire_rate = 60
        self.bullet_timer = 10
        self.current_sprite = flower_sprite

    @property
    def fire_effect(self):
        if not hasattr(self, '_fire_effect'):
            self._fire_effect = FlowerFire(self.body.position)
            self.scene.add_object(self._fire_effect)
        return self._fire_effect

    def deal_damage(self, damage):
        super().deal_damage(damage)
        if self.hp <= 0:
            self.fire_effect.stop()

    def update(self):
        super().update()
        self.fire_effect.update()
        self.bullet_timer += 1
        self.player = self.scene.find_player()
        if self.direct_sight(self.player) and self.bullet_timer > self.fire_rate:
            self.bullet_timer = 0
            self.shoot(self.player)

    def direct_sight(self, player):
        player_pos = player.body.position
        enemy_pos = self.body.position
        if player_pos.get_distance(enemy_pos) < 2000:
            query = self.scene.physics_space.segment_query_first([
                self.body.position.x, self.body.position.y], [player_pos.x, player_pos.y], 1,
                pymunk.ShapeFilter(mask=collision.Layer.BLOCK.value | collision.Layer.PLATFORM.value))
            if query:
                if query.shape.collision_type == collision.Layer.PLAYER.value:
                    return True
        return False

    def shoot(self, player):
        start = self.body.position
        stop = player.body.position
        direction = pygame.Vector2(stop) - pygame.Vector2(start)
        self.scene.add_object(EnemyBullet(start.x, start.y, direction, speed=1.2))
        enemy_shooting_sound.play()
        enemy_shooting_sound.set_volume(utils.controls['sound'])


class Spike(Solid):
    def __init__(self, position, properties=None):
        self.width = properties.get('width', 50)
        self.height = properties.get('height', 50)
        self.rotation = properties.get('rotationn', 0)
        super().__init__(position.x, position.y, self.width, self.height,
                         body_type=pymunk.Body.STATIC, layer=collision.Layer.SPIKE.value)
        self.image = scale_surface_contain(spike_wood_sprite, (self.width, self.height))
        if self.rotation != 0:
            self.image = pygame.transform.rotate(self.image, self.rotation)

    def draw(self, screen):
        screen.blit(self.image, self.scene.relative_position(pygame.Vector2(self.body.position) - pygame.Vector2(self.image.get_size()) / 2))

class SpikeTile(SolidTile):
    def __init__(self, position, image, colliders):
        super().__init__(
            position, image, colliders,
            layer=collision.Layer.SPIKE.value
        )
