import pygame

class Camera:
    def __init__(self, camera_func, initial_position, width, height):
        size = pygame.Vector2(width, height)
        self.rect = pygame.Rect(initial_position - size/2, size)
        self.update_func = camera_func
    
    def update(self):
        current_center = pygame.Vector2(self.rect.center)
        self.rect.center = pygame.Vector2.lerp(current_center, self.update_func(), 0.08)

    def relative_position_scaled(self, position, factor):
        offset = pygame.Vector2(
            self.rect.left * factor.x,
            self.rect.top * factor.y
        )
        return pygame.Vector2(position) + offset
    
    def relative_position(self, position):
        return pygame.Vector2(position) - pygame.Vector2(self.rect.topleft)

    def relative_rect(self, rect):
        return pygame.Rect(self.relative_position(rect.topleft), rect.size)
