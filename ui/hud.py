import pygame


class HUD:
    def __init__(self):
        self.heart_size = 32
        self.spacing = 8
        self.start_x = 20
        self.start_y = 20

        self.heart_full = pygame.image.load("assets/heart pixel art/heart pixel art 32x32.png").convert_alpha()
        self.heart_full = pygame.transform.scale(self.heart_full, (self.heart_size, self.heart_size))

        self.heart_empty = self.heart_full.copy()
        self.heart_empty.set_alpha(80)  # deixa transparente

        self.kill_icon = pygame.image.load("assets/enemies/vampire1/3.png").convert_alpha()

        # redimensiona (exemplo: 32x32)
        self.kill_icon = pygame.transform.scale(self.kill_icon, (32, 32))
        self.font = pygame.font.SysFont("arial", 28, bold=True)

    def draw(self, screen, player, kills):
        # corações (igual antes)
        for i in range(player.max_hp):
            x = self.start_x + i * (self.heart_size + self.spacing)
            y = self.start_y

            if i < player.hp:
                screen.blit(self.heart_full, (x, y))
            else:
                screen.blit(self.heart_empty, (x, y))

        # posição do contador
        icon_x = 20
        icon_y = 65

        screen.blit(self.kill_icon, (icon_x, icon_y))

        kills_text = self.font.render(f"x {kills}", True, (255, 255, 255))
        screen.blit(kills_text, (icon_x + 40, icon_y + 4))