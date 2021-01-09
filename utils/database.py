"""
Database handler for a CSV file.

CSV file format:
date,playtime,score,wave
"""

from datetime import datetime

STAT_FILE = "stats.txt"


def add_game(score, wave, playtime):
    """
    function that adds a game into file in CSV format
    """
    date = (str(datetime.now())).split()[0]
    with open(STAT_FILE, "a") as file:
        file.write(f"{date},{playtime},{score},{wave}\n")
