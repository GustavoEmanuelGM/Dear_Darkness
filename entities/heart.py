import pygame


class Heart:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/heart pixel art/heart pixel art 32x32.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (24, 24))

        self.rect = self.image.get_rect(center=(x, y))

        self.lifetime = 600  # dura 10 segundos (60fps)

    def update(self):
        self.lifetime -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_expired(self):
        return self.lifetime <= 0