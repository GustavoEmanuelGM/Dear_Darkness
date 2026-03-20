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
        self.is_attacking = False
        self.attack_pressed = False
        self.attack_active = False

        self.animations = {
            "idle_down": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_down.png", 8),
            "idle_up": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_up.png", 8),
            "idle_left": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_left.png", 8),
            "idle_right": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/IDLE/idle_right.png", 8),
            "walk_down": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/RUN/run_down.png", 8),
            "walk_up": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/RUN/run_up.png", 8),
            "walk_left": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/RUN/run_left.png", 8),
            "walk_right": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/RUN/run_right.png", 8),
            "attack_down": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/ATTACK 1/attack1_down.png", 8),
            "attack_up": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/ATTACK 1/attack1_up.png", 8),
            "attack_left": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/ATTACK 1/attack1_left.png", 8),
            "attack_right": self.load_frames("assets/Player/FREE_Adventurer 2D Pixel Art/Sprites/ATTACK 1/attack1_right.png", 8),
        }

        self.current_animation = "idle_down"
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.image = self.animations[self.current_animation][self.current_frame]

        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.hitbox = pygame.Rect(0, 0, 24, 14)
        self.hitbox.midbottom = (self.rect.centerx, self.rect.bottom - 4)

        self.sprite_offset_y = 6

        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)

        self.sync_rect_with_hitbox()

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

    def sync_rect_with_hitbox(self):
        self.rect.midbottom = (self.hitbox.centerx, self.hitbox.bottom + self.sprite_offset_y)

    def handle_input(self, world):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        self.is_moving = False

        if keys[pygame.K_SPACE]:
            if not self.attack_pressed and not self.is_attacking:
                self.is_attacking = True
                self.attack_pressed = True
                self.attack_active = False
                self.state = "attack"
                self.current_frame = 0
                self.animation_timer = 0
        else:
            self.attack_pressed = False

        if self.is_attacking:
            return

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

        self.move(dx, dy, world)

        if self.is_moving:
            self.state = "walk"
        else:
            self.state = "idle"

    def move(self, dx, dy, world):
        if dx != 0:
            new_hitbox = self.hitbox.move(dx, 0)
            if not self.collides_with_walls(new_hitbox, world):
                self.hitbox = new_hitbox

        if dy != 0:
            new_hitbox = self.hitbox.move(0, dy)
            if not self.collides_with_walls(new_hitbox, world):
                self.hitbox = new_hitbox

        self.sync_rect_with_hitbox()

    def collides_with_walls(self, hitbox, world):
        corners = [
            (hitbox.left, hitbox.top),
            (hitbox.right - 1, hitbox.top),
            (hitbox.left, hitbox.bottom - 1),
            (hitbox.right - 1, hitbox.bottom - 1),
        ]

        for x, y in corners:
            if world.is_blocked(x, y):
                return True

        return False

    def update_attack_hitbox(self):
        if not self.attack_active:
            self.attack_hitbox.size = (0, 0)
            return

        if self.direction == "down":
            self.attack_hitbox = pygame.Rect(
                self.hitbox.centerx - 18,
                self.hitbox.bottom - 4,
                36,
                28
            )

        elif self.direction == "up":
            self.attack_hitbox = pygame.Rect(
                self.hitbox.centerx - 18,
                self.hitbox.top - 55,
                36,
                28
            )

        elif self.direction == "left":
            self.attack_hitbox = pygame.Rect(
                self.hitbox.left - 34,
                self.hitbox.centery - 32,
                32,
                32
            )

        elif self.direction == "right":
            self.attack_hitbox = pygame.Rect(
                self.hitbox.right + 2,
                self.hitbox.centery - 32,
                32,
                32
            )

    def update_animation(self):
        new_animation = f"{self.state}_{self.direction}"

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0
            self.animation_timer = 0

        if self.state == "attack":
            animation_speed = 0.2
        else:
            animation_speed = self.animation_speed

        self.animation_timer += animation_speed

        if self.animation_timer >= 1:
            self.animation_timer = 0
            frames = self.animations[self.current_animation]

            if self.state == "attack":
                if self.current_frame < len(frames) - 1:
                    self.current_frame += 1
                else:
                    self.is_attacking = False
                    self.attack_active = False
                    self.state = "idle"
                    self.current_frame = 0
            else:
                self.current_frame = (self.current_frame + 1) % len(frames)

        if self.state == "attack":
            self.attack_active = 2 <= self.current_frame <= 4
        else:
            self.attack_active = False

        self.update_attack_hitbox()
        self.image = self.animations[self.current_animation][self.current_frame]

    def update(self, world):
        self.handle_input(world)
        self.update_animation()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # debug da hitbox do player
        # pygame.draw.rect(screen, (255, 255, 0), self.hitbox, 2)

        # debug da área de golpe
        if self.attack_active:
            pygame.draw.rect(screen, (255, 0, 0), self.attack_hitbox, 2)