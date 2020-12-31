import pygame
import os


WIDTH, HEIGHT = 1000, 750


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

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
