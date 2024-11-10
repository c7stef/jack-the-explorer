import pygame

class Camera:
    def __init__(self, camera_func, initial_position, width, height):
        size = pygame.Vector2(width, height)
        self.rect = pygame.Rect(initial_position - size/2, size)
        self.update_func = camera_func
        self.following = None
    
    def update(self):
        self.rect.center = self.update_func(self.following, pygame.Vector2(self.rect.center))

    def relative_position(self, position):
        return pygame.Vector2(position) - pygame.Vector2(self.rect.topleft)

    def relative_rect(self, rect):
        return pygame.Rect(self.relative_position(rect.topleft), rect.size)