"""
Star Wars PyGame, Space Invaders style

Main game file, run this file to start the game
"""

import time
import random
import pygame
from utils import database
from utils.load_assets import *
from utils.sound_control import *
from utils.leaderboard import create_leaderboard


WIDTH_H, HEIGHT_H = WIDTH // 2, HEIGHT // 2

# PyGame Setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Wars - Space Invaders")
main_font = pygame.font.Font("starjedi.ttf", 30)


class Laser:
    """
    controls laser drawing, movement, collisions and all events
    """

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
        return not height >= self.y >= 0

    def collision(self, obj):
        return collide(self, obj)


class PowerUP:
    """
    controls powerop drawing and type assigning
    """

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        types = {
            "speed": SPEED_PU,
            "health_player": HEALTH_PU,
            "health_lives": HEALTH_PU,
            "laser_speed": LASER_SPEED_PU,
            "enemy_freeze": ENEMY_FREEZE_PU,
        }
        self.pu_img = types[self.type]
        self.mask = pygame.mask.from_surface(self.pu_img)

    def draw(self, window):
        window.blit(self.pu_img, (self.x, self.y))


class Ship:
    """
    general ship class that controls ship events
    """

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
        """
        draws ship image and ship's lasers
        """
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        """
        moves ship lasers
        """
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
        """
        controls ships shoot cooldown
        """
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    """
    inherits from general ship class,
    this one has player specific properties like health bar
    """

    def __init__(self, x, y, ship_class):
        super().__init__(x, y)
        self.laser_img = LASER_BLUE_MED
        self.ship_class = ship_class

        ship_classes = {
            "classic": (ARC_170, 100, 30),
            "heavy": (LAAT, 150, 15),
            "scout": (JEDI_INTERCEPTOR, 80, 25),
            "sniper": (Y_WING, 100, 60),
        }
        self.ship_img, self.health, self.laser_cooldown = ship_classes[ship_class]
        self.max_health = self.health
        self.mask = pygame.mask.from_surface(self.ship_img)

    def player_regen(self):
        """
        regenerates player's health to full health
        """
        self.health = self.max_health

    def cooldown(self):
        """
        player cooldown based on it's ship type
        """
        if self.cool_down_counter >= self.laser_cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move_lasers(self, vel, objs):
        """
        moving player's lasers basen on ship type and checking for collisions
        """
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
        """
        draws ship image (from general ship class) and players health bar
        """
        super().draw(window)
        self.healthbar(window)

    def shoot(self):
        """
        gets laser position based on ship type and adds it to lasers list to be drawn
        """
        if self.cool_down_counter == 0:
            lasers_pos = {
                "classic": (self.x + 4, self.y + 30, self.x + 139, self.y + 30),
                "heavy": (self.x + 2, self.y + 50, self.x + 112, self.y + 50),
                "scout": (self.x + 35, self.y, self.x + 47, self.y),
                "sniper": (self.x + 22, self.y, self.x + 30, self.y),
            }

            laser = Laser(*lasers_pos[self.ship_class][:2], self.laser_img)
            self.lasers.append(laser)
            laser = Laser(*lasers_pos[self.ship_class][2:], self.laser_img)
            self.lasers.append(laser)

            self.cool_down_counter = 1

            if sfx_playing:
                SFX_PLAYER_FIRE.set_volume(0.2)
                SFX_PLAYER_FIRE.play()

    def healthbar(self, window):
        """
        draws players healthbar (green rect on top of red rect)
        """
        if self.health >= 0:
            pygame.draw.rect(
                window,
                (255, 0, 0),
                (
                    self.x,
                    self.y + self.ship_img.get_height() + 10,
                    self.ship_img.get_width(),
                    10,
                ),
            )
            pygame.draw.rect(
                window,
                (0, 255, 0),
                (
                    self.x,
                    self.y + self.ship_img.get_height() + 10,
                    self.ship_img.get_width() * (self.health / self.max_health),
                    10,
                ),
            )
        elif self.health < 0:
            pygame.draw.rect(
                window,
                (255, 0, 0),
                (
                    self.x,
                    self.y + self.ship_img.get_height() + 10,
                    self.ship_img.get_width(),
                    10,
                ),
            )


class Enemy(Ship):
    """
    inherits from general ship class,
    has specific needs for movement speed or shooting
    """

    COLOR_MAP = {
        "red": (CIS_FIGHTER, LASER_RED_SMALL),
        "green": (CIS_HYENA_BOMBER, LASER_RED_MED),
        "blue": (CIS_STRIKE_BOMBER, LASER_RED_MED),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        """
        method for enemy movement
        """
        self.y += vel

    def shoot(self):
        """
        method for enemy shooting
        """
        if self.y > 0:
            if self.cool_down_counter == 0:
                laser = Laser(self.x + 13, self.y + 15, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1
                if sfx_playing:
                    SFX_ENEMY_FIRE.set_volume(0.3)
                    SFX_ENEMY_FIRE.play()


def collide(obj1, obj2):
    """
    returns boolean if two given objects have collided
    """
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def ship_type(ship_class):
    """
    returns ship data based on the parameter
    """
    ship_classes = {
        "classic": (5, 6, "classic"),
        "heavy": (3, 4, "heavy"),
        "scout": (7, 8, "scout"),
        "sniper": (5, 12, "sniper"),
    }
    main(*ship_classes[ship_class])


def main(p_v, p_l_v, ship_class):
    """
    main game function, controls the whole game
    """
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

    start = time.time()

    def enemies_on_screen() -> int:
        """
        returns number of enemies currently on screen
        """
        n_of_enemies_on_screen = 0
        for enemy in enemies:
            if enemy.y > 0:
                n_of_enemies_on_screen += 1
        return int(n_of_enemies_on_screen)

    def redraw_window():
        """
        gets called every frame, redraws the game screen
        """
        WIN.blit(BG, (0, 0))

        # Draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Wave: {wave}", 1, (255, 255, 255))
        score_label = score_font.render(f"Score: {score}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (WIDTH_H - (score_label.get_width() // 2), 20))

        for e in enemies:
            e.draw(WIN)

        player.draw(WIN)

        if len(power_ups) >= 1:
            for p_u in power_ups:
                p_u.draw(WIN)

        if lost:
            lost_label = main_font.render("You lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH_H - lost_label.get_width() / 2, 350))
            final_score_label = main_font.render(
                f"Your score is {score}", 1, (255, 255, 255)
            )
            WIN.blit(
                final_score_label, (WIDTH_H - (final_score_label.get_width() / 2), 400)
            )

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
            if player.health < 0 and not player_sfx_played and sfx_playing:
                SFX_PLAYER_DESTROYED.set_volume(1)
                SFX_PLAYER_DESTROYED.play()
                player_sfx_played = True

        if lost:
            if lost_count > FPS * 3:
                playtime = round(time.time() - start, 2)
                database.add_game(score, wave, int(playtime))
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
                enemy = Enemy(
                    random.randrange(50, WIDTH - 100),
                    random.randrange(-1500, -100),
                    random.choice(["red", "blue", "green"]),
                )
                enemies.append(enemy)

            if wave != 1:
                if random.randrange(2) == 0:
                    avaible_pu_types = ["speed", "laser_speed"]

                    if player.health < 100 or lives < 5:
                        if player.health < 100:
                            avaible_pu_types.append("health_player")
                        elif lives < 5:
                            avaible_pu_types.append("health_lives")

                    pu_type = random.choice(avaible_pu_types)
                    power_up = PowerUP(
                        random.randrange(50, WIDTH - 50),
                        random.randrange(50, HEIGHT - 50),
                        pu_type,
                    )
                    power_ups.append(power_up)

        if enemies_on_screen() > 6:
            if freeze_active == 0:
                if random.randrange(2500) == 1:
                    if freeze_enemies == -1:
                        pu_type = "enemy_freeze"
                        power_up = PowerUP(
                            random.randrange(50, WIDTH - 50),
                            random.randrange(50, HEIGHT - 50),
                            pu_type,
                        )
                        power_ups.append(power_up)
                        freeze_active = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # move left
            player.x -= player_vel
        if (
            keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH
        ):  # move right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # move up
            player.y -= player_vel
        if (
            keys[pygame.K_s]
            and player.y + player_vel + player.get_height() + 15 < HEIGHT
        ):  # move down
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
    """
    TODO:
    difficulty
    save/do not save
    clear statistics with prompt
    """
    pass


def pause_menu():
    """
    creates and controls whole pause menu
    """
    click = False
    run = True

    while run:
        pos_x, pos_y = pygame.mouse.get_pos()

        # Menu Buttons
        button_resume = pygame.Rect(WIDTH_H - 130, HEIGHT_H - 80, 260, 50)
        button_main_menu = pygame.Rect(WIDTH_H - 130, HEIGHT_H, 260, 50)

        pygame.draw.rect(WIN, (204, 204, 204), button_resume)
        pygame.draw.rect(WIN, (204, 204, 204), button_main_menu)

        # Menu Labels
        label_resume = main_font.render("Resume", 1, (0, 47, 125))
        WIN.blit(label_resume, (WIDTH_H - 60, 295))

        label_main_menu = main_font.render("Main menu", 1, (0, 47, 125))
        WIN.blit(label_main_menu, (WIDTH_H - 90, 375))

        # Button Activations
        if click:
            if button_resume.collidepoint(pos_x, pos_y):
                run = False
            if button_main_menu.collidepoint(pos_x, pos_y):
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
    """
    creates and controls whole main menu
    """
    global music_playing
    global sfx_playing
    run = True
    click = False
    while run:
        WIN.blit(BG, (0, 0))

        pos_x, pos_y = pygame.mouse.get_pos()

        # Menu Buttons
        button_new_game = pygame.Rect(WIDTH_H - 130, HEIGHT_H - 80, 260, 50)
        button_change_ship = pygame.Rect(WIDTH_H - 130, HEIGHT_H, 260, 50)
        button_leave = pygame.Rect(WIDTH_H - 130, HEIGHT_H + 80, 260, 50)

        button_music = pygame.Rect(WIDTH - 150, 20, 50, 50)
        button_sfx = pygame.Rect(WIDTH - 80, 20, 50, 50)
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
            WIN.blit(MUSIC_ON, (WIDTH_H + 352, 25))
        else:
            WIN.blit(MUSIC_OFF, (WIDTH_H + 352, 25))

        if sfx_playing:
            WIN.blit(SFX_ON, (WIDTH_H + 422, 21))
        else:
            WIN.blit(SFX_OFF, (WIDTH_H + 422, 21))

        # Button Activations
        if button_new_game.collidepoint(pos_x, pos_y):
            if click:
                ship_type("classic")
        if button_leave.collidepoint(pos_x, pos_y):
            if click:
                break
        if button_change_ship.collidepoint(pos_x, pos_y):
            if click:
                change_ship_menu()
        if button_music.collidepoint(pos_x, pos_y):
            if click:
                if music_playing:
                    music_off()
                    music_playing = False
                else:
                    music_on()
                    music_playing = True
                main_menu()

        if button_sfx.collidepoint(pos_x, pos_y):
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
    """
    creates and controls whole menu where you can change your ship type
    """
    run = True
    click = False
    while run:
        WIN.blit(BG, (0, 0))

        pos_x, pos_y = pygame.mouse.get_pos()

        # Menu Buttons
        button_classic = pygame.Rect(WIDTH_H - 100, HEIGHT_H - 160, 200, 50)
        button_heavy = pygame.Rect(WIDTH_H - 100, HEIGHT_H - 80, 200, 50)
        button_scout = pygame.Rect(WIDTH_H - 100, HEIGHT_H, 200, 50)
        button_sniper = pygame.Rect(WIDTH_H - 100, HEIGHT_H + 80, 200, 50)

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

        if click:
            if button_classic.collidepoint(pos_x, pos_y):
                ship_type("classic")
            if button_heavy.collidepoint(pos_x, pos_y):
                ship_type("heavy")
            if button_scout.collidepoint(pos_x, pos_y):
                ship_type("scout")
            if button_sniper.collidepoint(pos_x, pos_y):
                ship_type("sniper")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
    pygame.quit()


if __name__ == "__main__":
    music_on()
    main_menu()
