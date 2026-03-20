import pygame
from pygame import Surface


class Enemy:
    def __init__(self, x: int, y: int) -> None:
        self.frame_width = 64
        self.frame_height = 64
        self.scale = 1



        self.width = self.frame_width * self.scale
        self.height = self.frame_height * self.scale

        self.speed = 2
        self.direction = "down"
        self.state = "idle"

        self.animations: dict[str, list[Surface]] = {
            # IDLE
            "idle_down": self.load_frames("assets/enemies/vampire1/Idle/Vampires1_Idle_full.png", 4, 0),
            "idle_right": self.load_frames("assets/enemies/vampire1/Idle/Vampires1_Idle_full.png", 4, 3),
            "idle_up": self.load_frames("assets/enemies/vampire1/Idle/Vampires1_Idle_full.png", 4, 1),
            "idle_left": self.load_frames("assets/enemies/vampire1/Idle/Vampires1_Idle_full.png", 4, 2),

            # WALK
            "walk_down": self.load_frames("assets/enemies/vampire1/Walk/Vampires1_Walk_full.png", 6, 0),
            "walk_right": self.load_frames("assets/enemies/vampire1/Walk/Vampires1_Walk_full.png", 6, 3),
            "walk_up": self.load_frames("assets/enemies/vampire1/Walk/Vampires1_Walk_full.png", 6, 1),
            "walk_left": self.load_frames("assets/enemies/vampire1/Walk/Vampires1_Walk_full.png", 6, 2),

            # HURT
            "hurt_down": self.load_frames("assets/enemies/vampire1/Hurt/Vampires1_Hurt_full.png", 4, 0),
            "hurt_right": self.load_frames("assets/enemies/vampire1/Hurt/Vampires1_Hurt_full.png", 4, 3),
            "hurt_up": self.load_frames("assets/enemies/vampire1/Hurt/Vampires1_Hurt_full.png", 4, 1),
            "hurt_left": self.load_frames("assets/enemies/vampire1/Hurt/Vampires1_Hurt_full.png", 4, 2),

            # DEATH
            "death_down": self.load_frames("assets/enemies/vampire1/Death/Vampires1_Death_full.png", 10, 0),
            "death_right": self.load_frames("assets/enemies/vampire1/Death/Vampires1_Death_full.png", 10, 3),
            "death_up": self.load_frames("assets/enemies/vampire1/Death/Vampires1_Death_full.png", 10, 1),
            "death_left": self.load_frames("assets/enemies/vampire1/Death/Vampires1_Death_full.png", 10, 2),
        }

        self.state = "idle"
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.15

        self.image: Surface = self.animations[f"{self.state}_{self.direction}"][0]

        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.hitbox = pygame.Rect(0, 0, 22, 14)
        self.hitbox.midbottom = self.rect.midbottom

        self.hp = 3
        self.alive = True
        self.damage_cooldown = 0

        self.follow_distance = 220

    def load_frames(self, path: str, frame_count: int, row: int = 0) -> list[Surface]:
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frames: list[Surface] = []

        for i in range(frame_count):
            frame_rect = pygame.Rect(
                i * self.frame_width,
                row * self.frame_height,
                self.frame_width,
                self.frame_height
            )

            frame = sprite_sheet.subsurface(frame_rect).copy()
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)

        return frames

    def take_damage(self) -> None:
        if not self.alive:
            return

        if self.state == "death":
            return

        if self.damage_cooldown > 0:
            return

        self.hp -= 1
        self.damage_cooldown = 20

        if self.hp <= 0:
            self.state = "death"
            self.current_frame = 0
            self.animation_timer = 0.0
        else:
            self.state = "hurt"
            self.current_frame = 0
            self.animation_timer = 0.0

    def collides_with_walls(self, hitbox: pygame.Rect, world) -> bool:
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

    def move_towards_player(self, player, world) -> None:
        if self.state in ("hurt", "death"):
            return

        dx = 0
        dy = 0

        enemy_x = self.hitbox.centerx
        enemy_y = self.hitbox.centery

        player_x = player.hitbox.centerx
        player_y = player.hitbox.centery

        distance_x = player_x - enemy_x
        distance_y = player_y - enemy_y

        if abs(distance_x) > self.follow_distance or abs(distance_y) > self.follow_distance:
            self.state = "idle"
            return

        if abs(distance_x) > 4:
            if distance_x > 0:
                dx = self.speed
                self.direction = "right"
            else:
                dx = -self.speed
                self.direction = "left"

        if abs(distance_y) > 4:
            if distance_y > 0:
                dy = self.speed
                self.direction = "down"
            else:
                dy = -self.speed
                self.direction = "up"

        moved = False

        if dx != 0:
            new_hitbox = self.hitbox.move(dx, 0)
            if not self.collides_with_walls(new_hitbox, world):
                self.hitbox = new_hitbox
                moved = True

        if dy != 0:
            new_hitbox = self.hitbox.move(0, dy)
            if not self.collides_with_walls(new_hitbox, world):
                self.hitbox = new_hitbox
                moved = True

        if moved:
            self.state = "walk"
        else:
            self.state = "idle"

    def update_animation(self) -> None:
        animation_key = f"{self.state}_{self.direction}"

        self.animation_timer += self.animation_speed

        if self.animation_timer >= 1:
            self.animation_timer = 0
            frames = self.animations[animation_key]

            if self.current_frame < len(frames) - 1:
                self.current_frame += 1
            else:
                if self.state == "hurt":
                    self.state = "idle"
                    self.current_frame = 0

                elif self.state == "death":
                    self.alive = False

                else:
                    self.current_frame = 0

        self.image = self.animations[animation_key][self.current_frame]
        self.rect.midbottom = self.hitbox.midbottom

    def update(self, player, world) -> None:
        if not self.alive and self.state != "death":
            return

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        self.move_towards_player(player, world)
        self.update_animation()

    def draw(self, screen: Surface) -> None:
        if self.alive:
            screen.blit(self.image, self.rect)

        # debug:
        # pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)