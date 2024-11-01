class GameObject:
    def set_scene(self, scene):
        self.scene = scene
    
    def collides_with(self, other):
        return self.rect.colliderect(other.rect)

    def update(self):
        raise NotImplementedError("Update method must be implemented by subclasses")

    def draw(self, screen):
        raise NotImplementedError("Draw method must be implemented by subclasses")
