"""
Module to control the sound effects / music
"""

import os
import random
import pygame

music_playing = True
sfx_playing = True


def music_on():
    """
    picks random song and turns it ON
    """

    # dict of avaible songs to choose, key is ID to list with filename and it's volume level
    songs = {
        0: ["force_theme.mp3", 1],
        1: ["anakins_betrayal.mp3", 1],
        2: ["battle_of_the_heroes.mp3", 5],
        3: ["duel of the fates.mp3", 0.6],
        4: ["]jedi_temple_march.mp3", 1],
    }

    SELECTED_SONG = songs[random.randrange(4)]
    pygame.mixer.music.load(os.path.join("assets/music", SELECTED_SONG[0]))
    pygame.mixer.music.set_volume(SELECTED_SONG[1])

    pygame.mixer.music.play(-1)


def music_off():
    """
    turns pygame music OFF
    """
    pygame.mixer.music.stop()
