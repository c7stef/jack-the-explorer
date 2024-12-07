import pygame
from gameobject import GameObject

from abc import ABC, abstractmethod

import numpy as np

class BackgroundImage(GameObject, ABC):
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


class BackgroundTint(BackgroundImage):
    def __init__(self, color, alpha=100, z_index=-5):
        self.z_index = z_index
        self.color = color
        self.alpha = alpha
    
    def create_surface(self, width, height):
        s = pygame.Surface((width, height))
        s.fill(self.color)
        s.set_alpha(self.alpha)
        return s

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

    print(gradient_data.shape)
    print(width, height)
    # Convert the numpy array to a Pygame surface
    pygame.surfarray.blit_array(gradient_surface, gradient_data)

    return gradient_surface

class BackgroundGradient(BackgroundImage):
    def __init__(self, color1, color2):
        self.z_index = -20
        self.color1 = color1
        self.color2 = color2
    
    def create_surface(self, width, height):
        return _create_radial_gradient(width, height, self.color1, self.color2)
