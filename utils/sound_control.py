import os
import random
import pygame

music_playing = True
sfx_playing = True


def music_on():
    rng = random.randrange(4)
    if rng == 0:
        FORCE_THEME = pygame.mixer.music.load(
            os.path.join("assets/music", "force_theme.mp3")
        )
        pygame.mixer.music.set_volume(1)
    elif rng == 1:
        ANAKINS_BETRAYAL = pygame.mixer.music.load(
            os.path.join("assets/music", "anakins_betrayal.mp3")
        )
        pygame.mixer.music.set_volume(1)
    elif rng == 2:
        BATTLE_OF_THE_HEROES = pygame.mixer.music.load(
            os.path.join("assets/music", "battle_of_the_heroes.mp3")
        )
        pygame.mixer.music.set_volume(5)
    elif rng == 3:
        DUEL_OF_THE_FATES = pygame.mixer.music.load(
            os.path.join("assets/music", "duel_of_the_fates.mp3")
        )
        pygame.mixer.music.set_volume(0.6)
    else:
        JEDI_TEMPLE_MARCH = pygame.mixer.music.load(
            os.path.join("assets/music", "jedi_temple_march.mp3")
        )
        pygame.mixer.music.set_volume(1)

    pygame.mixer.music.play(-1)


def music_off():
    pygame.mixer.music.stop()
