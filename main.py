import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE, BG_COLOR
from entities.player import Player
from maps.world import World
from entities.enemy import Enemy


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    world = World()
    player = Player(200, 200)
    enemy = Enemy(400, 300)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(world)
        enemy.update(player, world)

        if player.attack_active and enemy.alive:
            if player.attack_hitbox.colliderect(enemy.hitbox):
                enemy.take_damage()

        screen.fill(BG_COLOR)
        world.draw(screen)
        enemy.draw(screen)
        player.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()