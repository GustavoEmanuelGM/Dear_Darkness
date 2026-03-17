import pygame


class Player:
    def __init__(self, x, y):
        self.speed = 4

        self.frame_width = 96
        self.frame_height = 80
        self.scale = 1

        self.width = self.frame_width * self.scale
        self.height = self.frame_height * self.scale

        self.direction = "down"
        self.state = "idle"
        self.is_moving = False

        self.animations = {
            "idle_down": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_down.png", 8),
            "idle_up": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_up.png", 8),
            "idle_left": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_left.png", 8),
            "idle_right": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_right.png", 8),
            "walk_down": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/RUN/run_down.png", 8),
            "walk_up": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/RUN/run_up.png", 8),
            "walk_left": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/RUN/run_left.png", 8),
            "walk_right": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/RUN/run_right.png", 8),
        }

        self.current_animation = "idle_down"
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.image = self.animations[self.current_animation][self.current_frame]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def load_frames(self, path, frame_count):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frames = []

        for i in range(frame_count):
            frame_rect = pygame.Rect(
                i * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )
            frame = sprite_sheet.subsurface(frame_rect).copy()
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)

        return frames

    def handle_input(self):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        self.is_moving = False

        if keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
            self.is_moving = True
        elif keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
            self.is_moving = True

        if keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
            self.is_moving = True
        elif keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"
            self.is_moving = True

        self.rect.x += dx
        self.rect.y += dy

        if self.is_moving:
            self.state = "walk"
        else:
            self.state = "idle"

    def update_animation(self):
        new_animation = f"{self.state}_{self.direction}"

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0
            self.animation_timer = 0

        self.animation_timer += self.animation_speed

        if self.animation_timer >= 1:
            self.animation_timer = 0
            frames = self.animations[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(frames)

        self.image = self.animations[self.current_animation][self.current_frame]

    def update(self):
        self.handle_input()
        self.update_animation()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        screen.blit(self.image, self.rect)