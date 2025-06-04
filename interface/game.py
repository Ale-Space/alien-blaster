import pygame

class GAME:
    def __init__(self):
        self.musica_avviata = False

        self.font_path = "assets/font/RasterForgeRegular-JpBgm.ttf"
        self.font_titolo = pygame.font.Font(self.font_path, 115)
        self.font_info = pygame.font.Font(self.font_path, 40)  # Font per punteggio e vite

        self.titolo1 = self.font_titolo.render("GAME", True, (255, 255, 255))
        self.titolo2 = self.font_titolo.render("STARTED", True, (255, 255, 255))

        self.count_scritte = 0
        self.time_scritte = 30
        self.scritte = True

        self.x_title = None
        self.x_title2 = None
        self.y_title = None

        self.punteggio = 0  # Inizializza il punteggio

    def avvia_musica(self):
        if not self.musica_avviata:
            pygame.mixer.music.load("assets/audio/Game.mp3")
            pygame.mixer.music.play(-1)
            self.musica_avviata = True

    def ferma_musica(self):
        if self.musica_avviata:
            pygame.mixer.music.stop()
            self.musica_avviata = False

    def scritta_schermo(self, game_screen, display_width, display_height):
        if self.x_title is None or self.x_title2 is None or self.y_title is None:
            self.y_title = display_height // 2 - self.titolo1.get_height() // 2
            self.x_title = display_width // 2 - self.titolo1.get_width() - 95
            self.x_title2 = display_width // 2 - 45

        if self.scritte:
            game_screen.blit(self.titolo1, (self.x_title, self.y_title))
            game_screen.blit(self.titolo2, (self.x_title2, self.y_title))

            self.count_scritte += 1
            if self.count_scritte >= self.time_scritte:
                self.x_title -= 20
                self.x_title2 += 25

            if self.x_title2 < -self.titolo1.get_width():
                self.scritte = False

    def mostra_punteggio_vite(self, game_screen, players, display_width):
        # Punteggio
        punteggio_txt = self.font_info.render(f"SCORE: {self.punteggio}", True, (255, 255, 255))
        game_screen.blit(punteggio_txt, (display_width // 2 - punteggio_txt.get_width() // 2, 10))

        # Vite
        if hasattr(players, 'player0') and players.player0:
            vite0 = getattr(players, 'lives0', 4)
            txt0 = self.font_info.render(f"P1: {vite0}♥", True, (0, 200, 255))
            game_screen.blit(txt0, (10, 10))

        if hasattr(players, 'player1') and players.player1:
            vite1 = getattr(players, 'lives1', 4)
            txt1 = self.font_info.render(f"P2: {vite1}♥", True, (255, 100, 100))
            game_screen.blit(txt1, (10, 60))

        if hasattr(players, 'player2') and players.player2:
            vite2 = getattr(players, 'lives2', 4)
            txt2 = self.font_info.render(f"P3: {vite2}♥", True, (255, 255, 100))
            game_screen.blit(txt2, (10, 110))

    def check_collisions(self, players, enemies):
        for enemy in enemies:
            for bullet in enemy.bullets[:]:
                bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet['width'], bullet['height'])

                if players.player0:
                    player0_rect = pygame.Rect(players.x0, players.y0,
                                               players.player0_image.get_width(), players.player0_image.get_height())
                    if player0_rect.colliderect(bullet_rect):
                        enemy.bullets.remove(bullet)
                        players.lives0 = getattr(players, 'lives0', 4) - 1
                        if players.lives0 <= 0:
                            print("Player 0 morto!")
                            players.player0 = False
                        continue

                if players.player1:
                    player1_rect = pygame.Rect(players.x1, players.y1,
                                               players.player1_image.get_width(), players.player1_image.get_height())
                    if player1_rect.colliderect(bullet_rect):
                        enemy.bullets.remove(bullet)
                        players.lives1 = getattr(players, 'lives1', 4) - 1
                        if players.lives1 <= 0:
                            print("Player 1 morto!")
                            players.player1 = False
                        continue

                if players.player2:
                    player2_rect = pygame.Rect(players.x2, players.y2,
                                               players.player2_image.get_width(), players.player2_image.get_height())
                    if player2_rect.colliderect(bullet_rect):
                        enemy.bullets.remove(bullet)
                        players.lives2 = getattr(players, 'lives2', 4) - 1
                        if players.lives2 <= 0:
                            print("Player 2 morto!")
                            players.player2 = False
                        continue

        def check_enemy_hit(proiettili):
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                for proiettile in proiettili[:]:
                    bullet_pos = proiettile["pos"]
                    bullet_rect = pygame.Rect(bullet_pos[0], bullet_pos[1],
                                              players.bullet_frame[0].get_width(), players.bullet_frame[0].get_height())
                    if enemy_rect.colliderect(bullet_rect):
                        proiettili.remove(proiettile)
                        if enemy.strength == "weak":
                            enemy.lives -= 1
                        else:
                            enemy.lives -= 0.5
                        if enemy.lives <= 0:
                            enemies.remove(enemy)
                            self.punteggio += 100  # +100 punti per nemico ucciso
                        break

        if players.player0:
            check_enemy_hit(players.player0_bullet)
        if players.player1:
            check_enemy_hit(players.player1_bullet)
        if players.player2:
            check_enemy_hit(players.player2_bullet)