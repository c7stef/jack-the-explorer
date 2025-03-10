import pygame
from gameobject import GameObject
import particlepy
import random

from abc import ABC, abstractmethod

import numpy as np

class ImageOverlay(GameObject, ABC):
    def update(self):
        pass

    @abstractmethod
    def create_surface(self, width, height):
        raise NotImplementedError("surface() must be implemented by subclasses")
    
    def surface(self, width, height):
        if not hasattr(self, '_surface'):
            self._surface = self.create_surface(width, height)
        return self._surface
    
    def draw(self, screen):
        w = screen.get_width()
        h = screen.get_height()

        surface = self.surface(w, h)
        screen.blit(surface, (0, 0))


class TintEffect(ImageOverlay):
    def __init__(self, color, alpha=100, z_index=-5):
        self.z_index = z_index
        self.color = color
        self.alpha = alpha
    
    def create_surface(self, width, height):
        s = pygame.Surface((width, height))
        s.fill(self.color)
        s.set_alpha(self.alpha)
        return s


class BgImage(ImageOverlay):
    def __init__(self, image_path, tile_size):
        self.z_index = -10
        self.image_path = image_path
        self.tile_size = tile_size
    
    def create_surface(self, width, height):
        return pygame.image.load(self.image_path)

    @property
    def size(self):
        return self.surface(0, 0).get_size()

    def draw(self, screen):
        position = pygame.Vector2(0, 0)
        bg_size = pygame.Vector2(self.size) - self.tile_size
        screen.blit(self.surface(0, 0), self.scene.relative_position_parallax(position, bg_size))

def _create_radial_gradient(width, height, color_start, color_end):
    # Create an empty surface for the gradient
    gradient_surface = pygame.Surface((width, height))

    # Convert the start and end colors into numpy arrays
    color_start = np.array(color_start)
    color_end = np.array(color_end)

    # Create arrays for the X and Y coordinates
    y = np.arange(height)
    x = np.arange(width)

    # Create a meshgrid for the coordinates (X, Y) for all pixels
    Y, X = np.meshgrid(y, x)

    # Calculate the distance from the center for each pixel
    center_x, center_y = width // 2, height // 2
    dist = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)

    # Normalize the distance (0 is the center, max is the farthest corner)
    max_dist = np.sqrt(center_x ** 2 + center_y ** 2)
    normalized_dist = dist / max_dist

    # Interpolate between the start and end color based on the normalized distance
    r = np.uint8(color_start[0] + (color_end[0] - color_start[0]) * normalized_dist)
    g = np.uint8(color_start[1] + (color_end[1] - color_start[1]) * normalized_dist)
    b = np.uint8(color_start[2] + (color_end[2] - color_start[2]) * normalized_dist)

    # Stack the R, G, B channels together to form an RGB image
    gradient_data = np.stack((r, g, b), axis=-1)

    # Convert the numpy array to a Pygame surface
    pygame.surfarray.blit_array(gradient_surface, gradient_data)

    return gradient_surface

class BackgroundGradient(ImageOverlay):
    def __init__(self, color1, color2):
        self.z_index = -20
        self.color1 = color1
        self.color2 = color2
    
    def create_surface(self, width, height):
        return _create_radial_gradient(width, height, self.color1, self.color2)

class BackgroundParticles(GameObject):
    def __init__(self):
        self.z_index = -1
        self.particle_system = particlepy.particle.ParticleSystem()
        self.relative_position = pygame.Vector2(0, 0)
    
    def update(self):
        self.particle_system.update(1/120)

        screen_width, screen_height = self.scene.map_bounds.size

        self.particle_system.emit(
            particlepy.particle.Particle(
                shape=particlepy.shape.Circle(
                    radius=random.randint(5, 10),
                    color=(255, 255, 255),
                    alpha=100),
                position=(random.uniform(0, screen_width), random.uniform(0, screen_height)),
                velocity=(random.uniform(-15, 15), random.uniform(-15, 15)),
                
                delta_radius=0.2))

        # color manipulation
        for particle in self.particle_system.particles:
            particle.shape.color = particlepy.math.fade_color(
                particle=particle,
                color=(255, 255, 255),
                progress=particle.inverted_progress)
            particle.shape.alpha = particlepy.math.fade_alpha(particle, 0, progress=particle.inverted_progress)

        # render shapes
        self.particle_system.make_shape()

        parallax_size = pygame.Vector2(screen_width, screen_height) * 0.7

        # post shape creation manipulation
        for particle in self.particle_system.particles:
            particle.position += self.scene.relative_position_parallax((0, 0), parallax_size) - self.relative_position
        
        self.relative_position = self.scene.relative_position_parallax((0, 0), parallax_size)

    def draw(self, screen):
        self.particle_system.render(surface=screen)
    
