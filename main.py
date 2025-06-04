import pygame
import sys
from object_game import PLAYER
from interface import MENU, GAME

# Importa la classe ENEMY e EnemyInstance (se sono in file separato, importali correttamente)
from object_game import ENEMY  # metti il nome file giusto

pygame.init()

display_width = 1200
display_height = 800

display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption("ALIEN BLASTER")

game_screen = pygame.Surface((display_width, display_height))

fps = 60
clock = pygame.time.Clock()

state_menu = True
state_game = False

menu = MENU()
game = GAME()
player = PLAYER()

menu.resize_background(display_width, display_height)

# --- INIZIO INTEGRAZIONE NEMICI ---
enemy_factory = ENEMY()
enemies = []
spawn_timer = 0
spawn_interval = 90  # genera nemico ogni 90 frame (1.5 secondi a 60fps)
# --- FINE INTEGRAZIONE NEMICI ---

frame_count = 0
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            display_width, display_height = event.w, event.h
            display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
            game_screen = pygame.Surface((display_width, display_height))
            menu.resize_background(display_width, display_height)

    game_screen.fill((0, 0, 0))

    if state_menu:
        menu.avvia_musica()
        menu.background(game_screen)
        menu.scritte_bg(game_screen, display_width, display_height)
        menu.bottoni(game_screen, display_width, display_height)
        menu.check_mouse_events(events)

        display.blit(game_screen, (0, 0))

        if menu.start and menu.scelto in [1, 2]:
            state_menu = False
            state_game = True
            menu.ferma_musica()
            game.avvia_musica()

            # Inizializza il giocatore solo UNA volta
            player.scelto = menu.scelto
            player.init_position(display_width, display_height)

    elif state_game:
        menu.background(game_screen) 
        game.scritta_schermo(game_screen, display_width, display_height)
        game.mostra_punteggio_vite(game_screen, player, display_width)


        player.move_player(display_width, display_height)
        player.draw(game_screen)
        player.check_player_death()
        player.gestisci_sparo()
        player.aggiorna(game_screen, display_width)
        game.check_collisions(player,enemies)

        # --- INIZIO INTEGRAZIONE NEMICI ---

        # Genera nemici a intervalli regolari, assicurandosi che non si sovrappongano
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            new_enemy = enemy_factory.generate_enemy(display_width, display_height, enemies)
            enemies.append(new_enemy)

        # Aggiorna e disegna nemici e i loro proiettili
        frame_count += 1
        for enemy in enemies:
            enemy.update(frame_count)
            enemy.draw(game_screen)

        # Rimuovi nemici usciti dallo schermo a sinistra
        enemies = [e for e in enemies if e.x + e.width > 0]

        # --- FINE INTEGRAZIONE NEMICI ---

        display.blit(game_screen, (0, 0))

    pygame.display.update()
    clock.tick(fps)
