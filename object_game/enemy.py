import pygame
import random

class ENEMY:
    def __init__(self):
        self.villain_1 = pygame.transform.scale(
            pygame.image.load("assets/immagini/villain_base1.png"), (80, 80))
        
        self.villain_2 = pygame.transform.scale(
            pygame.image.load("assets/immagini/villain_base2.png"), (80, 80))
        
        self.villain_3 = pygame.transform.scale(
            pygame.image.load("assets/immagini/villain_1.png"), (90, 90))
        
        self.villain_4 = pygame.transform.scale(
            pygame.image.load("assets/immagini/villain_2.png"), (90, 90))

        # Velocità iniziale più alta per weak, più bassa per strong
        self.speed_weak = 3.5    # più veloce per i weak
        self.speed_strong = 3    # un po' più lento per i strong
        self.bullet_speed = 10

        self.bullet_frame = [
            pygame.transform.scale(
            pygame.image.load("assets/immagini/blast1.png"), (60, 30)),
            pygame.transform.scale(
            pygame.image.load("assets/immagini/blast2.png"), (60, 30)),
            pygame.transform.scale(
            pygame.image.load("assets/immagini/blast3.png"), (60, 30)),
            pygame.transform.scale(
            pygame.image.load("assets/immagini/blast4.png"), (60, 30)),
            pygame.transform.scale(
            pygame.image.load("assets/immagini/blast5.png"), (60, 30))
        ]

    def generate_enemy(self, display_width, display_height, existing_enemies):
        enemy_types = [
            (self.villain_1, 80, 80, "weak"),
            (self.villain_2, 80, 80, "weak"),
            (self.villain_3, 90, 90, "strong"),
            (self.villain_4, 90, 90, "strong")
        ]
        weights = [0.4, 0.4, 0.1, 0.1]

        img, w, h, strength = random.choices(enemy_types, weights)[0]

        if strength == "weak":
            speed = self.speed_weak
            bullet_speed = self.bullet_speed
        else:
            speed = self.speed_strong
            bullet_speed = self.bullet_speed + 4

        max_tries = 20
        for _ in range(max_tries):
            y = random.randint(0, display_height - h)
            overlaps = False
            for e in existing_enemies:
                if (display_width < e.x + e.width and display_width + w > e.x and
                    y < e.y + e.height and y + h > e.y):
                    overlaps = True
                    break
            if not overlaps:
                break
        else:
            y = 0

        x = display_width

        return EnemyInstance(img, x, y, w, h, speed, bullet_speed, strength, self.bullet_frame)


class EnemyInstance:
    def __init__(self, image, x, y, width, height, speed, bullet_speed, strength, bullet_frames):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.strength = strength
        self.bullet_frames = bullet_frames
        self.bullets = []
        if self.strength == "weak":
            self.lives = 1
        elif self.strength == "strong":
            self.lives = 2


        self.shoot_cooldown = 0
        self.shots_in_burst = 0

        self.burst_size = 3 if self.strength == "strong" else 1
        self.burst_pause = 120

        # Parametri per animazione colpi
        self.bullet_frame_index = 0

        # Parametri base per difficoltà crescente
        self.base_speed = speed
        self.base_bullet_speed = bullet_speed
        self.base_burst_pause = self.burst_pause
        self.base_shoot_cooldown = 60 if self.strength == "weak" else 10

    def update(self, game_frame_count):
        self.adjust_difficulty(game_frame_count)
        self.x -= self.speed

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            if self.strength == "strong":
                if self.shots_in_burst < self.burst_size:
                    self.shoot()
                    self.shots_in_burst += 1
                    self.shoot_cooldown = self.base_shoot_cooldown
                else:
                    self.shoot_cooldown = self.burst_pause
                    self.shots_in_burst = 0
            else:
                if random.random() < 0.01:
                    self.shoot()
                    self.shoot_cooldown = self.base_shoot_cooldown

        # Aggiorna animazione e posizione proiettili nemici
        for bullet in self.bullets[:]:
            bullet['x'] -= self.bullet_speed

            # Gestione animazione frame proiettile
            if 'frame_index' not in bullet:
                bullet['frame_index'] = 0
                bullet['frame_count'] = 0
                bullet['image'] = self.bullet_frames[0]

            bullet['frame_count'] += 1
            if bullet['frame_count'] >= 3:  # cambia frame ogni 3 tick
                if bullet['frame_index'] < len(self.bullet_frames) - 1:
                    bullet['frame_index'] += 1
                    bullet['image'] = self.bullet_frames[bullet['frame_index']]
                bullet['frame_count'] = 0

        # Rimuove proiettili fuori schermo
        self.bullets = [b for b in self.bullets if b['x'] > -b['width']]    

    def adjust_difficulty(self, game_frame_count):
        level = game_frame_count // 3600  # ogni 60 sec (a 60fps)

        # Aumenta velocità fino al +50%
        self.speed = min(self.base_speed * (1 + 0.1 * level), self.base_speed * 1.5)

        # Diminuisce pausa burst fino a metà
        self.burst_pause = max(int(self.base_burst_pause * (1 - 0.1 * level)), int(self.base_burst_pause / 2))

        # Aumenta velocità proiettili fino al +50%
        self.bullet_speed = min(self.base_bullet_speed * (1 + 0.1 * level), self.base_bullet_speed * 1.5)

        # Riduce cooldown sparo fino a metà
        self.base_shoot_cooldown = max(int(self.base_shoot_cooldown * (1 - 0.1 * level)), int(self.base_shoot_cooldown / 2))

    def shoot(self):
        bullet_image = self.bullet_frames[self.bullet_frame_index]
        self.bullet_frame_index = (self.bullet_frame_index + 1) % len(self.bullet_frames)

        bullet_width = bullet_image.get_width()
        bullet_height = bullet_image.get_height()

        bullet_x = self.x
        bullet_y = self.y + self.height // 2 - bullet_height // 2

        self.bullets.append({'image': bullet_image, 'x': bullet_x, 'y': bullet_y, 'width': bullet_width, 'height': bullet_height})

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            screen.blit(bullet['image'], (bullet['x'], bullet['y']))