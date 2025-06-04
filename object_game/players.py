import pygame

class PLAYER:
    def __init__(self):
        # Coordinate iniziali (posizioni verranno impostate da init_position)
        self.x0 = self.y0 = None
        self.x1 = self.y1 = None
        self.x2 = self.y2 = None

        # Scelta modalità 1 o 2 giocatori
        self.scelto = 0

        self.player0 = False
        self.player1 = False
        self.player2 = False

        # Caricamento immagini giocatori e creazione maschere per collisioni
        self.player0_image = pygame.transform.scale(
            pygame.image.load("assets/immagini/ship-0.png"), (110, 110))
        self.player1_image = pygame.transform.scale(
            pygame.image.load("assets/immagini/ship-blue.png"), (110, 110))
        self.player2_image = pygame.transform.scale(
            pygame.image.load("assets/immagini/ship-red.png"), (110, 110))
        
        self.mask0 = pygame.mask.from_surface(self.player0_image)
        self.mask1 = pygame.mask.from_surface(self.player1_image)
        self.mask2 = pygame.mask.from_surface(self.player2_image)

        # Vite iniziali
        self.lives0 = 4
        self.lives1 = 4
        self.lives2 = 4

        self.player_speed = 5

        # Proiettili e animazioni sparo
        self.bullet_frame = [
            pygame.transform.scale(
            pygame.image.load("assets/immagini/colpo_1.png"), (60, 30)),
            pygame.transform.scale(
            pygame.image.load("assets/immagini/colpo_2.png"), (60, 30)),
            pygame.transform.scale(
            pygame.image.load("assets/immagini/colpo_3.png"), (60, 30)),
            pygame.transform.scale(
            pygame.image.load("assets/immagini/colpo_4.png"), (60, 30)),
            pygame.transform.scale(
            pygame.image.load("assets/immagini/colpo_5.png"), (60, 30))
        ]

        self.player0_bullet = []
        self.player1_bullet = []
        self.player2_bullet = []

        self.bullet_speed = 12
        self.bullet_waiting = 20

        self.bullet_wait_c = 0
        self.bullet_wait_ctrl = 0

        self.animation_speed = 3

        self.shot_sound = pygame.mixer.Sound("assets/audio/effetto_1.mp3")

    def init_position(self, display_width, display_height):
        # Inizializza coordinate giocatori in base alla scelta
        if self.scelto == 1:
            self.x0 = display_width // 5
            self.y0 = display_height // 2
            self.player0 = True
            self.player1 = False
            self.player2 = False
        elif self.scelto == 2:
            self.x1 = display_width // 5
            self.y1 = display_height // 2 - 80
            self.x2 = display_width // 5
            self.y2 = display_height // 2 + 80
            self.player0 = False
            self.player1 = True
            self.player2 = True

    def move_player(self, display_width, display_height):
        keys = pygame.key.get_pressed()

        # PLAYER 0 (single player mode)
        if self.player0:
            if keys[pygame.K_w] and self.y0 > 0:
                self.y0 -= self.player_speed
            if keys[pygame.K_s] and self.y0 < display_height - 110:
                self.y0 += self.player_speed
            if keys[pygame.K_d] and self.x0 < display_width // 4:
                self.x0 += self.player_speed
            if keys[pygame.K_a] and self.x0 > 0:
                self.x0 -= self.player_speed

        # PLAYER 1 (blu, in multiplayer)
        if self.player1:
            # Controlla collisione con player2 solo se player2 è vivo
            collide_check = (lambda x, y: self.collide(x, y, self.x2, self.y2, self.mask1, self.mask2)) if self.player2 else (lambda x, y: False)

            if keys[pygame.K_w] and self.y1 > 0:
                if not collide_check(self.x1, self.y1 - self.player_speed):
                    self.y1 -= self.player_speed
            if keys[pygame.K_s] and self.y1 < display_height - 110:
                if not collide_check(self.x1, self.y1 + self.player_speed):
                    self.y1 += self.player_speed
            if keys[pygame.K_d] and self.x1 < display_width // 4:
                if not collide_check(self.x1 + self.player_speed, self.y1):
                    self.x1 += self.player_speed
            if keys[pygame.K_a] and self.x1 > 0:
                if not collide_check(self.x1 - self.player_speed, self.y1):
                    self.x1 -= self.player_speed

        # PLAYER 2 (rosso, in multiplayer)
        if self.player2:
            collide_check = (lambda x, y: self.collide(x, y, self.x1, self.y1, self.mask2, self.mask1)) if self.player1 else (lambda x, y: False)

            if keys[pygame.K_UP] and self.y2 > 0:
                if not collide_check(self.x2, self.y2 - self.player_speed):
                    self.y2 -= self.player_speed
            if keys[pygame.K_DOWN] and self.y2 < display_height - 110:
                if not collide_check(self.x2, self.y2 + self.player_speed):
                    self.y2 += self.player_speed
            if keys[pygame.K_RIGHT] and self.x2 < display_width // 4:
                if not collide_check(self.x2 + self.player_speed, self.y2):
                    self.x2 += self.player_speed
            if keys[pygame.K_LEFT] and self.x2 > 0:
                if not collide_check(self.x2 - self.player_speed, self.y2):
                    self.x2 -= self.player_speed

    def collide(self, x1, y1, x2, y2, mask_a=None, mask_b=None):
        if mask_a is None or mask_b is None:
            return False
        offset = (int(x2 - x1), int(y2 - y1))
        return mask_a.overlap(mask_b, offset) is not None

    def check_player_death(self):
        # Disattiva player e maschere se vite a 0 o meno
        if self.lives0 <= 0 and self.player0:
            self.player0 = False
            self.x0 = None
            self.y0 = None
            self.mask0 = None

        if self.lives1 <= 0 and self.player1:
            self.player1 = False
            self.x1 = None
            self.y1 = None
            self.mask1 = None

        if self.lives2 <= 0 and self.player2:
            self.player2 = False
            self.x2 = None
            self.y2 = None
            self.mask2 = None

    def draw(self, game_screen):
        if self.player0:
            game_screen.blit(self.player0_image, (self.x0, self.y0))
        if self.player1:
            game_screen.blit(self.player1_image, (self.x1, self.y1))
        if self.player2:
            game_screen.blit(self.player2_image, (self.x2, self.y2))

    def draw_shot(self, x, y, id):
        centro_x = x + 110
        centro_y = y + 55
        nuovo_proiettile = {
            "pos": [centro_x, centro_y],
            "frame_index": 0,
            "frame_count": 0
        }
        if id == 0:
            if len(self.player0_bullet) < 3:
                self.player0_bullet.append(nuovo_proiettile)
                self.shot_sound.play()
        elif id == 1:
            if len(self.player1_bullet) < 3:
                self.player1_bullet.append(nuovo_proiettile)
                self.shot_sound.play()
        elif id == 2:
            if len(self.player2_bullet) < 3:
                self.player2_bullet.append(nuovo_proiettile)
                self.shot_sound.play()

    def aggiorna(self, game_screen, display_width):
        if self.player0:
            self.aggiorna_lista(game_screen, display_width, self.player0_bullet)
        if self.player1:
            self.aggiorna_lista(game_screen, display_width, self.player1_bullet)
        if self.player2:
            self.aggiorna_lista(game_screen, display_width, self.player2_bullet)

    def aggiorna_lista(self, game_screen, display_width, lista):
        for proiettile in lista[:]:
            proiettile["pos"][0] += self.bullet_speed

            if proiettile["frame_index"] < len(self.bullet_frame) - 1:
                proiettile["frame_count"] += 1
                if proiettile["frame_count"] >= self.animation_speed:
                    proiettile["frame_index"] += 1
                    proiettile["frame_count"] = 0

            image = self.bullet_frame[proiettile["frame_index"]]
            image_rect = image.get_rect(center=proiettile["pos"])
            game_screen.blit(image, image_rect)

            if proiettile["pos"][0] > display_width:
                lista.remove(proiettile)

    def gestisci_sparo(self):
        keys = pygame.key.get_pressed()

        self.bullet_wait_c += 1
        self.bullet_wait_ctrl += 1

        if keys[pygame.K_c] and self.bullet_wait_c > self.bullet_waiting:
            if self.player0:
                self.draw_shot(self.x0, self.y0, 0)
            if self.player1:
                self.draw_shot(self.x1, self.y1, 1)
            self.bullet_wait_c = 0

        if keys[pygame.K_RCTRL] and self.bullet_wait_ctrl > self.bullet_waiting:
            if self.player2:
                self.draw_shot(self.x2, self.y2, 2)
            self.bullet_wait_ctrl = 0




                

                


            






                    
