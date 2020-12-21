# 15.4.2020
# Star Wars PyGame, Space Invaders style

import pygame
import os
import random

from utils import database

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# PyGame Setup
WIDTH, HEIGHT = 1000, 750
MID_W, MID_H = WIDTH // 2, HEIGHT // 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Wars - Space Invaders")
main_font = pygame.font.Font("starjedi.ttf", 30)

# Loading Icons
MUSIC_ON = pygame.image.load(os.path.join("assets/menu_icons", "music_on.png"))
MUSIC_ON = pygame.transform.scale(MUSIC_ON, (40, 40))
MUSIC_OFF = pygame.image.load(os.path.join("assets/menu_icons", "music_off.png"))
MUSIC_OFF = pygame.transform.scale(MUSIC_OFF, (40, 40))

SFX_ON = pygame.image.load(os.path.join("assets/menu_icons", "sfx_on.png"))
SFX_ON = pygame.transform.scale(SFX_ON, (50, 50))
SFX_OFF = pygame.image.load(os.path.join("assets/menu_icons", "sfx_off.png"))
SFX_OFF = pygame.transform.scale(SFX_OFF, (50, 50))

# Loading Ship Images
CIS_FIGHTER = pygame.image.load(
    os.path.join("assets/skins", "cis_fighter.png"))
CIS_HYENA_BOMBER = pygame.image.load(
    os.path.join("assets/skins", "cis_hyena_bomber.png"))
CIS_STRIKE_BOMBER = pygame.image.load(
    os.path.join("assets/skins", "cis_strike_bomber.png"))

# Player Ships
ARC_170 = pygame.image.load(
    os.path.join("assets/skins", "arc_170.png"))
ARC_170 = pygame.transform.scale(ARC_170, (150, 150))
LAAT = pygame.image.load(
    os.path.join("assets/skins", "laat.png"))
Y_WING = pygame.image.load(
    os.path.join("assets/skins", "y_wing.png"))
JEDI_INTERCEPTOR = pygame.image.load(
    os.path.join("assets/skins", "jedi_interceptor.png"))

# Lasers
LASER_RED_SMALL = pygame.image.load(
    os.path.join("assets/lasers", "laser_red_small.png"))
LASER_RED_MED = pygame.image.load(
    os.path.join("assets/lasers", "laser_red_med.png"))
LASER_BLUE_MED = pygame.image.load(
    os.path.join("assets/lasers", "laser_blue_med.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Power Ups
SPEED_PU = pygame.image.load(os.path.join("assets/power_ups", "speed_pu.png"))
HEALTH_PU = pygame.image.load(os.path.join("assets/power_ups", "health_pu.png"))
LASER_SPEED_PU = pygame.image.load(
    os.path.join("assets/power_ups", "laser_speed_pu.png"))
ENEMY_FREEZE_PU = pygame.image.load(
    os.path.join("assets/power_ups", "enemy_freeze_pu.png"))

# SFX
SFX_EXPLOSION_1 = pygame.mixer.Sound(os.path.join("assets/sfx", "explosion_1.wav"))
SFX_PLAYER_FIRE = pygame.mixer.Sound(os.path.join("assets/sfx", "player_fire.wav"))
SFX_ENEMY_FIRE = pygame.mixer.Sound(os.path.join("assets/sfx", "enemy_fire.wav"))
SFX_PLAYER_DESTROYED = pygame.mixer.Sound(
    os.path.join("assets/sfx", "player_explode.wav"))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Power_up:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        if self.type == "speed":
            self.pu_img = SPEED_PU
        elif self.type == "health_player" or self.type == "health_lives":
            self.pu_img = HEALTH_PU
        elif self.type == "laser_speed":
            self.pu_img = LASER_SPEED_PU
        elif self.type == "enemy_freeze":
            self.pu_img = ENEMY_FREEZE_PU

        self.mask = pygame.mask.from_surface(self.pu_img)

    def draw(self, window):
        window.blit(self.pu_img, (self.x, self.y))


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
                # TODO: add SFX of player ship hit

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, ship_class):
        super().__init__(x, y)
        self.laser_img = LASER_BLUE_MED
        self.ship_class = ship_class

        if ship_class == "classic":
            self.ship_img = ARC_170
            self.health = 100
            self.laser_cooldown = 30
        elif ship_class == "heavy":
            self.ship_img = LAAT
            self.health = 150
            self.laser_cooldown = 15
        elif ship_class == "scout":
            self.ship_img = JEDI_INTERCEPTOR
            self.health = 80
            self.laser_cooldown = 25
        elif ship_class == "sniper":
            self.ship_img = Y_WING
            self.health = 100
            self.laser_cooldown = 60

        self.max_health = self.health
        self.mask = pygame.mask.from_surface(self.ship_img)

    def get_player_health(self):
        return self.health

    def player_regen(self):
        self.health = self.max_health

    def cooldown(self):
        if self.cool_down_counter >= self.laser_cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def shoot(self):
        if self.cool_down_counter == 0:

            if self.ship_class == "classic":
                laser = Laser(self.x + 4, self.y + 30, self.laser_img)
                self.lasers.append(laser)
                laser = Laser(self.x + self.ship_img.get_width() -
                              11, self.y + 30, self.laser_img)
                self.lasers.append(laser)

            elif self.ship_class == "heavy":
                laser = Laser(self.x + 2, self.y + 50, self.laser_img)
                self.lasers.append(laser)
                laser = Laser(self.x + self.ship_img.get_width() -
                              8, self.y + 50, self.laser_img)
                self.lasers.append(laser)

            elif self.ship_class == "scout":
                laser = Laser(self.x + 35, self.y, self.laser_img)
                self.lasers.append(laser)
                laser = Laser(self.x + self.ship_img.get_width() -
                              41, self.y, self.laser_img)
                self.lasers.append(laser)

            elif self.ship_class == "sniper":
                laser = Laser(self.x + 22, self.y, self.laser_img)
                self.lasers.append(laser)
                laser = Laser(self.x + 30, self.y, self.laser_img)
                self.lasers.append(laser)

            self.cool_down_counter = 1

            if sfx_playing:
                SFX_PLAYER_FIRE.set_volume(0.2)
                SFX_PLAYER_FIRE.play()

    def healthbar(self, window):
        if self.health >= 0:
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                                   self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() +
                                                   10, self.ship_img.get_width() * (self.health / self.max_health), 10))
        elif self.health < 0:
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                                   self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (CIS_FIGHTER, LASER_RED_SMALL),
        "green": (CIS_HYENA_BOMBER, LASER_RED_MED),
        "blue": (CIS_STRIKE_BOMBER, LASER_RED_MED)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.y > 0:
            if self.cool_down_counter == 0:
                laser = Laser(self.x + 13, self.y + 15, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1
                if sfx_playing:
                    SFX_ENEMY_FIRE.set_volume(0.3)
                    SFX_ENEMY_FIRE.play()

    def get_y(self):
        return self.y


def music_on():
    rng = random.randrange(4)
    if rng == 0:
        FORCE_THEME = pygame.mixer.music.load(os.path.join("assets/music", "force_theme.mp3"))
        pygame.mixer.music.set_volume(1)
    elif rng == 1:
        ANAKINS_BETRAYAL = pygame.mixer.music.load(os.path.join("assets/music", "anakins_betrayal.mp3"))
        pygame.mixer.music.set_volume(1)
    elif rng == 2:
        BATTLE_OF_THE_HEROES = pygame.mixer.music.load(os.path.join("assets/music", "battle_of_the_heroes.mp3"))
        pygame.mixer.music.set_volume(5)
    elif rng == 3:
        DUEL_OF_THE_FATES = pygame.mixer.music.load(os.path.join("assets/music", "duel_of_the_fates.mp3"))
        pygame.mixer.music.set_volume(0.6)
    else:
        JEDI_TEMPLE_MARCH = pygame.mixer.music.load(os.path.join("assets/music", "jedi_temple_march.mp3"))
        pygame.mixer.music.set_volume(1)

    pygame.mixer.music.play(-1)


def music_off():
    pygame.mixer.music.stop()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def ship_type(ship_class):
    if ship_class == "classic":
        main(5, 6, "classic")
    elif ship_class == "heavy":
        main(3, 4, "heavy")
    elif ship_class == "scout":
        main(7, 8, "scout")
    elif ship_class == "sniper":
        main(5, 12, "sniper")


def main(p_v, p_l_v, ship_class):
    player_sfx_played = False
    run = True
    FPS = 60
    wave = 0
    lives = 5
    score = 0
    s = 0
    score_font = pygame.font.Font("starjedi.ttf", 20)

    enemies = []
    power_ups = []
    wave_lenght = 5
    enemy_vel = 1
    enemy_laser_vel = 5

    player_vel = p_v
    player_laser_vel = p_l_v
    player = Player(450, 500, ship_class)

    power_up_duration = -1
    freeze_enemies = -1
    freeze_active = 0

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def enemies_on_screen():
        n_of_enemies_on_screen = 0
        for enemy in enemies:
            if enemy.get_y() > 0:
                n_of_enemies_on_screen += 1
        return int(n_of_enemies_on_screen)

    def redraw_window():
        WIN.blit(BG, (0, 0))

        # Draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Wave: {wave}", 1, (255, 255, 255))
        score_label = score_font.render(f"Score: {score}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (MID_W - (score_label.get_width() // 2), 20))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if len(power_ups) >= 1:
            for power_up in power_ups:
                power_up.draw(WIN)

        if lost:
            lost_label = main_font.render("Game Over!", 1, (255, 255, 255))
            WIN.blit(lost_label, (MID_W - lost_label.get_width() / 2, 350))
            final_score_label = main_font.render(
                f"Your score is {score}", 1, (255, 255, 255))
            WIN.blit(final_score_label, (MID_W -
                                         (final_score_label.get_width() // 2), 400))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        if not lost:
            if s % FPS == 0:
                score += 1
            s += 1

        if lives <= 0 or player.health < 0:
            lost = True
            lost_count += 1
            if player.health < 0 and player_sfx_played == False and sfx_playing:
                SFX_PLAYER_DESTROYED.set_volume(1)
                SFX_PLAYER_DESTROYED.play()
                player_sfx_played = True

        if lost:
            if lost_count > FPS * 3:
                database.add_game(score, wave)
                run = False
            else:
                continue

        # No enemies alive
        if len(enemies) == 0:
            wave += 1

            # Enemy laser vel increase
            if wave % 4 == 0:
                enemy_laser_vel += 1

            # Enemy vel increase
            if wave % 6 == 0:
                enemy_vel += 1
            wave_lenght += 3
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(
                    50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

            if wave != 1:
                if random.randrange(2) == 0:
                    avaible_pu_types = ["speed", "laser_speed"]

                    if player.get_player_health() < 100 or lives < 5:
                        if player.get_player_health() < 100:
                            avaible_pu_types.append("health_player")
                        elif lives < 5:
                            avaible_pu_types.append("health_lives")

                    pu_type = random.choice((avaible_pu_types))
                    power_up = Power_up(random.randrange(
                        50, WIDTH - 50), random.randrange(50, HEIGHT - 50), pu_type)
                    power_ups.append(power_up)

        if enemies_on_screen() > 6:
            if freeze_active == 0:
                if random.randrange(2500) == 1:
                    if freeze_enemies == -1:
                        pu_type = "enemy_freeze"
                        power_up = Power_up(random.randrange(
                            50, WIDTH - 50), random.randrange(50, HEIGHT - 50), pu_type)
                        power_ups.append(power_up)
                        freeze_active = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # move left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # move right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # move up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # move down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            pause_menu()

        for enemy in enemies[:]:
            if freeze_enemies == -1:
                enemy.move(enemy_vel)
                enemy.move_lasers(enemy_laser_vel, player)
                freeze_active = 0

            if freeze_active == 0:
                if random.randrange(0, 2 * FPS) == 1:
                    enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            if enemy.y + enemy.get_height() > HEIGHT + 30:
                lives -= 1
                enemies.remove(enemy)

        if 240 >= freeze_enemies >= 0:
            freeze_enemies -= 1

        for power_up in power_ups:
            if collide(player, power_up):
                power_ups.remove(power_up)
                power_up_duration = 240

        if power_up_duration == 240:
            if pu_type == "enemy_freeze":
                freeze_enemies = 240
                freeze_active = 1
            elif pu_type == "speed":
                player_vel += 4
            elif pu_type == "health_lives":
                lives += 1
            elif pu_type == "health_player":
                player.player_regen()
            elif pu_type == "laser_speed":
                player_laser_vel += 4
            power_up_duration -= 1

        elif 240 > power_up_duration > 0:
            power_up_duration -= 1

        elif power_up_duration == 0:
            if pu_type == "speed":
                player_vel -= 4
            elif pu_type == "laser_speed":
                player_laser_vel -= 4
            power_up_duration = -1

        player.move_lasers(-player_laser_vel, enemies)


def settings_menu():
    '''
    TODO:
    difficulty
    save/do not save
    clear statistics with prompt
    '''
    pass


def pause_menu():
    click = False
    run = True

    while run:
        pos_x, pos_y = pygame.mouse.get_pos()

        # Menu Buttons
        button_resume = pygame.Rect(
            MID_W - 130, MID_H - 80, 260, 50)
        button_settings = pygame.Rect(
            MID_W - 130, MID_H, 260, 50)
        button_main_menu = pygame.Rect(
            MID_W - 130, MID_H + 80, 260, 50)

        pygame.draw.rect(WIN, (204, 204, 204), button_resume)
        pygame.draw.rect(WIN, (204, 204, 204), button_settings)
        pygame.draw.rect(WIN, (204, 204, 204), button_main_menu)

        # Menu Labels
        label_resume = main_font.render("Resume", 1, (0, 47, 125))
        WIN.blit(label_resume, (MID_W - 60, 295))

        label_settings = main_font.render("Settings", 1, (0, 47, 125))
        WIN.blit(label_settings, (MID_W - 75, 375))

        label_main_menu = main_font.render("Main menu", 1, (0, 47, 125))
        WIN.blit(label_main_menu, (MID_W - 90, 455))

        # Button Activations
        if button_resume.collidepoint((pos_x, pos_y)):
            if click:
                run = False
        if button_settings.collidepoint((pos_x, pos_y)):
            if click:
                settings_menu()
        if button_main_menu.collidepoint((pos_x, pos_y)):
            if click:
                run = False
                main_menu()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False


def main_menu():
    global music_playing
    global sfx_playing
    run = True
    click = False
    while run:
        WIN.blit(BG, (0, 0))

        pos_x, pos_y = pygame.mouse.get_pos()

        # Menu Buttons
        button_new_game = pygame.Rect(
            MID_W - 130, MID_H - 80, 260, 50)
        button_change_ship = pygame.Rect(
            MID_W - 130, MID_H, 260, 50)
        button_leave = pygame.Rect(
            MID_W - 130, MID_H + 80, 260, 50)
        button_music = pygame.Rect(
            (WIDTH) - 150, 20, 50, 50)
        button_sfx = pygame.Rect(
            (WIDTH) - 80, 20, 50, 50)
        pygame.draw.rect(WIN, (204, 204, 204), button_new_game)
        pygame.draw.rect(WIN, (204, 204, 204), button_leave)
        pygame.draw.rect(WIN, (204, 204, 204), button_change_ship)
        pygame.draw.rect(WIN, (204, 204, 204), button_sfx)
        pygame.draw.rect(WIN, (204, 204, 204), button_music)

        # Menu Labels
        label_new_game = main_font.render("New Game", 1, (0, 47, 125))
        WIN.blit(label_new_game, (417, 295))

        label_change_ship = main_font.render("Change Ship", 1, (0, 47, 125))
        WIN.blit(label_change_ship, (398, 375))

        label_leave = main_font.render("Leave", 1, (0, 47, 125))
        WIN.blit(label_leave, (445, 455))

        # Menu Icons
        if music_playing:
            WIN.blit(MUSIC_ON, (MID_W + 352, 25))
        else:
            WIN.blit(MUSIC_OFF, (MID_W + 352, 25))

        if sfx_playing:
            WIN.blit(SFX_ON, (MID_W + 422, 21))
        else:
            WIN.blit(SFX_OFF, (MID_W + 422, 21))

        # Button Activations
        if button_new_game.collidepoint((pos_x, pos_y)):
            if click:
                ship_type("classic")
        if button_leave.collidepoint((pos_x, pos_y)):
            if click:
                break
                quit()
        if button_change_ship.collidepoint((pos_x, pos_y)):
            if click:
                change_ship_menu()
        if button_music.collidepoint((pos_x, pos_y)):
            if click:
                if music_playing:
                    music_off()
                    music_playing = False
                else:
                    music_on()
                    music_playing = True
                main_menu()

        if button_sfx.collidepoint((pos_x, pos_y)):
            if click:
                if sfx_playing:
                    sfx_playing = False
                else:
                    sfx_playing = True
                main_menu()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
    pygame.quit()


def change_ship_menu():
    run = True
    click = False
    while run:
        WIN.blit(BG, (0, 0))

        pos_x, pos_y = pygame.mouse.get_pos()

        # Menu Buttons
        button_classic = pygame.Rect(
            MID_W - 100, MID_H - 160, 200, 50)
        button_heavy = pygame.Rect(
            MID_W - 100, MID_H - 80, 200, 50)
        button_scout = pygame.Rect(
            MID_W - 100, MID_H, 200, 50)
        button_sniper = pygame.Rect(
            MID_W - 100, MID_H + 80, 200, 50)
        pygame.draw.rect(WIN, (204, 204, 204), button_classic)
        pygame.draw.rect(WIN, (204, 204, 204), button_heavy)
        pygame.draw.rect(WIN, (204, 204, 204), button_scout)
        pygame.draw.rect(WIN, (204, 204, 204), button_sniper)

        # Menu labels
        label_classic = main_font.render("Classic", 1, (0, 47, 125))
        WIN.blit(label_classic, (435, 215))
        label_heavy = main_font.render("Heavy", 1, (0, 47, 125))
        WIN.blit(label_heavy, (445, 295))
        label_scout = main_font.render("Scout", 1, (0, 47, 125))
        WIN.blit(label_scout, (440, 375))
        label_sniper = main_font.render("Sniper", 1, (0, 47, 125))
        WIN.blit(label_sniper, (438, 455))

        if button_classic.collidepoint((pos_x, pos_y)):
            if click:
                ship_type("classic")
        if button_heavy.collidepoint((pos_x, pos_y)):
            if click:
                ship_type("heavy")
        if button_scout.collidepoint((pos_x, pos_y)):
            if click:
                ship_type("scout")
        if button_sniper.collidepoint((pos_x, pos_y)):
            if click:
                ship_type("sniper")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
    pygame.quit()


music_playing = True
sfx_playing = True
music_on()
main_menu()
