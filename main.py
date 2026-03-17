import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE, BG_COLOR
from entities.player import Player


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    player = Player(200, 200)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()

        screen.fill(BG_COLOR)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()