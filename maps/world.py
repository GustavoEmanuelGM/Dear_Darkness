import pygame
from settings import WIDTH, HEIGHT


class World:
    def __init__(self):
        self.map_image = pygame.image.load("assets/dungeon sangrenta full.png").convert()
        self.map_image = pygame.transform.scale(self.map_image, (WIDTH, HEIGHT))

        self.blocked_rects = [
            pygame.Rect(0, 0, WIDTH, 100),
            pygame.Rect(0, HEIGHT - 50, WIDTH, 32),
            pygame.Rect(0, 0, 32, HEIGHT),
            pygame.Rect(WIDTH - 32, 0, 32, HEIGHT),
        ]

        self.blocked_rects.append(pygame.Rect(0, HEIGHT - 90, 260, 90))
        self.blocked_rects.append(pygame.Rect(WIDTH - 260, HEIGHT - 90, 260, 90))

    def draw(self, screen):
        screen.blit(self.map_image, (0, 0))

        # debug
        # for rect in self.blocked_rects:
        #     pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    def is_blocked(self, x, y):
        point = (x, y)

        for rect in self.blocked_rects:
            if rect.collidepoint(point):
                return True

        return False

    def rect_is_blocked(self, rect):
        for blocked in self.blocked_rects:
            if rect.colliderect(blocked):
                return True
        return False