import random
import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE, BG_COLOR
from entities.player import Player
from maps.world import World
from entities.enemy import Enemy
from entities.heart import Heart
from ui.hud import HUD


MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
SCORES = "scores"


def spawn_enemy(world, player):
    enemy_rect = pygame.Rect(0, 0, 22, 14)

    margin = 120
    min_distance_from_player = 140

    for _ in range(100):
        x = random.randint(margin, WIDTH - margin)
        y = random.randint(margin, HEIGHT - margin)

        enemy_rect.center = (x, y)

        if world.rect_is_blocked(enemy_rect):
            continue

        dx = player.hitbox.centerx - x
        dy = player.hitbox.centery - y

        if abs(dx) < min_distance_from_player and abs(dy) < min_distance_from_player:
            continue

        return Enemy(x, y)

    return Enemy(WIDTH // 2, HEIGHT // 2)


def reset_game():
    world = World()
    player = Player(200, 200)
    enemies = [Enemy(400, 300)]
    drops = []
    spawn_timer = 0
    spawn_delay = 120
    max_enemies = 10
    kills = 0

    return world, player, enemies, drops, spawn_timer, spawn_delay, max_enemies, kills


def draw_menu_option(screen, text, font, x, y, selected):
    if selected:
        color = (255, 255, 255)
        shadow_color = (120, 255, 120)
        prefix = "> "
    else:
        color = (180, 180, 180)
        shadow_color = (40, 40, 40)
        prefix = "  "

    label = prefix + text

    shadow = font.render(label, True, shadow_color)
    shadow_rect = shadow.get_rect(center=(x + 2, y + 2))
    screen.blit(shadow, shadow_rect)

    surf = font.render(label, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    hud = HUD()

    font_menu = pygame.font.SysFont("arial", 34, bold=True)
    font_small = pygame.font.SysFont("arial", 24)
    font_big = pygame.font.SysFont("arial", 64, bold=True)
    font_score = pygame.font.SysFont("arial", 30, bold=True)

    # fundos
    menu_bg = pygame.image.load("assets/Dear Darkness.png").convert()
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

    game_over_bg = pygame.image.load("assets/GAME OVER SCREEN .png").convert()
    game_over_bg = pygame.transform.scale(game_over_bg, (WIDTH, HEIGHT))

    # sons e músicas
    menu_music_path = "assets/sounds/DavidKBD-04 - Devoured by Darkness.ogg"
    battle_music_path = "assets/sounds/DavidKBD-Mini Loop 12.ogg"

    attack_sound = pygame.mixer.Sound("assets/sounds/knifesharpener1.flac")
    game_over_sound = pygame.mixer.Sound("assets/sounds/DavidKBD-02 - Blood Soaked Earth.ogg")
    enemy_death_sound = pygame.mixer.Sound("assets/sounds/morte dos vampiros.wav")

    attack_sound.set_volume(0.5)
    game_over_sound.set_volume(0.7)
    enemy_death_sound.set_volume(2.0)
    pygame.mixer.music.set_volume(0.5)

    current_music = None
    game_over_sound_played = False

    def play_music(track_path):
        nonlocal current_music
        if current_music != track_path:
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play(-1)
            current_music = track_path

    game_state = MENU
    best_score = 0

    world, player, enemies, drops, spawn_timer, spawn_delay, max_enemies, kills = reset_game()

    menu_options = ["NOVO JOGO", "SCORES", "EXIT GAME"]
    selected_option = 0

    game_over_options = ["VOLTAR AO MENU"]
    selected_game_over_option = 0

    running = True
    while running:
        clock.tick(FPS)

        # controle de música por estado
        if game_state in (MENU, SCORES):
            play_music(menu_music_path)
        elif game_state == PLAYING:
            play_music(battle_music_path)
        elif game_state == GAME_OVER:
            if current_music is not None:
                pygame.mixer.music.stop()
                current_music = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_state == MENU:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        selected_option = (selected_option - 1) % len(menu_options)

                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        selected_option = (selected_option + 1) % len(menu_options)

                    elif event.key == pygame.K_SPACE:
                        choice = menu_options[selected_option]

                        if choice == "NOVO JOGO":
                            world, player, enemies, drops, spawn_timer, spawn_delay, max_enemies, kills = reset_game()
                            game_state = PLAYING
                            game_over_sound_played = False

                        elif choice == "SCORES":
                            game_state = SCORES

                        elif choice == "EXIT GAME":
                            running = False

                elif game_state == GAME_OVER:
                    if event.key in (pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN):
                        selected_game_over_option = 0

                    elif event.key == pygame.K_SPACE:
                        game_state = MENU
                        selected_option = 0
                        game_over_sound_played = False

                elif game_state == SCORES:
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                        game_state = MENU
                        selected_option = 0

        if game_state == PLAYING:
            spawn_timer += 1
            if spawn_timer >= spawn_delay and len(enemies) < max_enemies:
                enemies.append(spawn_enemy(world, player))
                spawn_timer = 0

            was_attacking = player.is_attacking
            player.update(world)

            if not was_attacking and player.is_attacking:
                attack_sound.stop()
                attack_sound.play()

            for enemy in enemies:
                enemy.update(player, world)

            if player.attack_active:
                for enemy in enemies:
                    if enemy.alive and player.attack_hitbox.colliderect(enemy.hitbox):
                        enemy.take_damage()

            if player.hp > 0:
                for enemy in enemies:
                    if enemy.alive and enemy.hitbox.colliderect(player.hitbox):
                        player.take_damage(1)

            dead_enemies = [enemy for enemy in enemies if not enemy.alive]

            if dead_enemies:
                enemy_death_sound.play()

            for enemy in dead_enemies:
                kills += 1

                if random.random() < 0.3:
                    drops.append(Heart(enemy.hitbox.centerx, enemy.hitbox.centery))

            enemies = [enemy for enemy in enemies if enemy.alive]

            for drop in drops:
                drop.update()

            drops = [drop for drop in drops if not drop.is_expired()]

            for drop in drops[:]:
                if player.hitbox.colliderect(drop.rect):
                    if player.hp < player.max_hp:
                        player.hp += 1
                    drops.remove(drop)

            if player.hp <= 0:
                if kills > best_score:
                    best_score = kills

                game_state = GAME_OVER

                if not game_over_sound_played:
                    game_over_sound.play()
                    game_over_sound_played = True

                selected_game_over_option = 0

        screen.fill(BG_COLOR)

        if game_state == MENU:
            screen.blit(menu_bg, (0, 0))

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 60))
            screen.blit(overlay, (0, 0))

            menu_center_x = WIDTH // 2
            start_y = HEIGHT - 180
            spacing = 50

            for i, option in enumerate(menu_options):
                y = start_y + i * spacing
                draw_menu_option(
                    screen,
                    option,
                    font_menu,
                    menu_center_x,
                    y,
                    i == selected_option
                )

            help_text = font_small.render("W/S ou Setas para mover • ESPACO para confirmar", True, (220, 220, 220))
            help_rect = help_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
            screen.blit(help_text, help_rect)

        elif game_state == PLAYING:
            world.draw(screen)

            for enemy in enemies:
                enemy.draw(screen)

            for drop in drops:
                drop.draw(screen)

            player.draw(screen)
            hud.draw(screen, player, kills)

        elif game_state == GAME_OVER:
            screen.blit(game_over_bg, (0, 0))

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))

            text_kills = font_score.render(f"Kills: {kills}", True, (255, 255, 255))
            text_best = font_score.render(f"Best Score: {best_score}", True, (220, 220, 220))

            screen.blit(text_kills, (WIDTH // 2 - text_kills.get_width() // 2, HEIGHT - 170))
            screen.blit(text_best, (WIDTH // 2 - text_best.get_width() // 2, HEIGHT - 130))

            draw_menu_option(
                screen,
                game_over_options[0],
                font_menu,
                WIDTH // 2,
                HEIGHT - 65,
                True
            )

            help_text = font_small.render("ESPACO para confirmar", True, (220, 220, 220))
            help_rect = help_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
            screen.blit(help_text, help_rect)

        elif game_state == SCORES:
            screen.blit(menu_bg, (0, 0))

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            title_surface = font_big.render("SCORES", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(WIDTH // 2, 130))
            screen.blit(title_surface, title_rect)

            best_surface = font_score.render(f"Melhor score da sessao: {best_score}", True, (255, 255, 255))
            best_rect = best_surface.get_rect(center=(WIDTH // 2, 250))
            screen.blit(best_surface, best_rect)

            back_text = font_menu.render("ESPACO para voltar", True, (220, 220, 220))
            back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 90))
            screen.blit(back_text, back_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()