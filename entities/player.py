import pygame


class Player:
    def __init__(self, x, y):
        self.speed = 4

        self.frame_width = 96
        self.frame_height = 80

        self.scale = 1
        self.width = self.frame_width * self.scale
        self.height = self.frame_height * self.scale

        self.sprite_sheet = pygame.image.load("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_down.png").convert_alpha()

        # cria lista de frames
        self.frames = self.load_frames()

        # animação
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.image = self.frames[self.current_frame]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def load_frames(self):
        frames = []
        for i in range(8):  # 8 frames
            frame_rect = pygame.Rect(
                i * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )

            frame = self.sprite_sheet.subsurface(frame_rect).copy()
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)

        return frames

    def animate(self):
        self.animation_timer += self.animation_speed

        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        self.image = self.frames[self.current_frame]

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

    def update(self):
        self.handle_input()
        self.animate()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        screen.blit(self.image, self.rect)