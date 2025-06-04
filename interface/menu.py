import pygame

import pygame

class MENU:
    def __init__(self):

        # BACKGROUND
        self.background_path = "assets/immagini/BackGround.jpg"
        self.background_image_orig = pygame.image.load(self.background_path).convert_alpha()
        self.background_image = self.background_image_orig

        self.x1_bg = 0
        self.x2_bg = self.background_image.get_width()
        self.speed = 2

        self.musica_avviata = False

        # FONT E TESTI
        self.font_path = "assets/font/RasterForgeRegular-JpBgm.ttf"
        self.font_titolo = pygame.font.Font(self.font_path, 115)
        self.font_scritte = pygame.font.Font(self.font_path, 40)
        self.testo_titolo = self.font_titolo.render("ALIEN BLASTERS", True, (255, 255, 255))
        self.testo_chose = self.font_scritte.render("Select Players", True, (255, 0, 0))

        # BOTTONI
        self.button_size = (225, 125)
        self.chose_sound = pygame.mixer.Sound("assets/audio/chose.mp3")
        self.start_sound = pygame.mixer.Sound("assets/audio/start.mp3")


        # Player1
        self.player1_img_normal = pygame.image.load("assets/immagini/1player.png").convert_alpha()
        self.player1_img_hover = pygame.image.load("assets/immagini/1player_selected.png").convert_alpha()
        self.player1_img_normal = pygame.transform.scale(self.player1_img_normal, self.button_size)
        self.player1_img_hover = pygame.transform.scale(self.player1_img_hover, self.button_size)

        # Player2
        self.player2_img_normal = pygame.image.load("assets/immagini/2players.png").convert_alpha()
        self.player2_img_hover = pygame.image.load("assets/immagini/2players_selected.png").convert_alpha()
        self.player2_img_normal = pygame.transform.scale(self.player2_img_normal, self.button_size)
        self.player2_img_hover = pygame.transform.scale(self.player2_img_hover, self.button_size)

        # Start
        self.start_img_normal = pygame.image.load("assets/immagini/start.png").convert_alpha()
        self.start_img_hover = pygame.image.load("assets/immagini/start_selected.png").convert_alpha()
        self.start_img_normal = pygame.transform.scale(self.start_img_normal, self.button_size)
        self.start_img_hover = pygame.transform.scale(self.start_img_hover, self.button_size)

        # Stato selezioni
        self.scelto = 0
        self.start = False

        # Rettangoli bottoni
        self.pl1_rect = None
        self.pl2_rect = None
        self.start_rect = None

    def avvia_musica(self):
        if not self.musica_avviata:
            pygame.mixer.music.load("assets/audio/Menu.mp3")
            pygame.mixer.music.play(-1)
            self.musica_avviata = True

    def ferma_musica(self):
        if self.musica_avviata:
            pygame.mixer.music.stop()
            self.musica_avviata = False

    def resize_background(self, display_width, display_height):
        self.background_image = pygame.transform.scale(self.background_image_orig, (display_width, display_height))
        self.x1_bg = 0
        self.x2_bg = self.background_image.get_width()

    def background(self, game_screen):
        # Movimento sfondo
        self.x1_bg -= self.speed
        self.x2_bg -= self.speed

        if self.x1_bg <= -self.background_image.get_width():
            self.x1_bg = self.x2_bg + self.background_image.get_width()

        if self.x2_bg <= -self.background_image.get_width():
            self.x2_bg = self.x1_bg + self.background_image.get_width()

        # Disegno sfondo
        game_screen.blit(self.background_image, (self.x1_bg, 0))
        game_screen.blit(self.background_image, (self.x2_bg, 0))

    def scritte_bg(self, game_screen, display_width, display_height):
        x_titolo = display_width // 2 - self.testo_titolo.get_width() // 2
        x_chose = display_width // 2 - self.testo_chose.get_width() // 2

        y_titolo = display_height // 5
        y_chose = display_height // 3 + display_height // 12

        game_screen.blit(self.testo_titolo, (x_titolo, y_titolo))
        game_screen.blit(self.testo_chose, (x_chose, y_chose))

    def bottoni(self, game_screen, display_width, display_height):
        y_pl = display_height // 2

        x_pl1 = display_width // 4
        x_pl2 = display_width // 2 + display_width // 4 - self.button_size[0]

        x_strt = display_width // 2 - self.button_size[0] // 2
        y_strt = display_height // 2 + display_height // 5

        # Aggiorna rettangoli per mouse
        self.pl1_rect = self.player1_img_normal.get_rect(topleft=(x_pl1, y_pl))
        self.pl2_rect = self.player2_img_normal.get_rect(topleft=(x_pl2, y_pl))
        self.start_rect = self.start_img_normal.get_rect(topleft=(x_strt, y_strt))

        mouse_pos = pygame.mouse.get_pos()

        # Player1
        if self.pl1_rect.collidepoint(mouse_pos):
            game_screen.blit(self.player1_img_hover, (x_pl1, y_pl))
        else:
            game_screen.blit(self.player1_img_normal, (x_pl1, y_pl))

        # Player2
        if self.pl2_rect.collidepoint(mouse_pos):
            game_screen.blit(self.player2_img_hover, (x_pl2, y_pl))
        else:
            game_screen.blit(self.player2_img_normal, (x_pl2, y_pl))

        # Start
        if self.start_rect.collidepoint(mouse_pos):
            game_screen.blit(self.start_img_hover, (x_strt, y_strt))
        else:
            game_screen.blit(self.start_img_normal, (x_strt, y_strt))

        # Evidenzia scelta attiva
        if self.scelto == 1:
            game_screen.blit(self.player1_img_hover, (x_pl1, y_pl))
        elif self.scelto == 2:
            game_screen.blit(self.player2_img_hover, (x_pl2, y_pl))

        if self.start:
            game_screen.blit(self.start_img_hover, (x_strt, y_strt))

    def check_mouse_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.pl1_rect and self.pl1_rect.collidepoint(mouse_pos):
                    self.scelto = 1
                    self.chose_sound.play()
                elif self.pl2_rect and self.pl2_rect.collidepoint(mouse_pos):
                    self.scelto = 2
                    self.chose_sound.play()
                elif self.start_rect and self.start_rect.collidepoint(mouse_pos) and self.scelto in [1, 2]:
                    self.start = True
                    self.start_sound.play()
