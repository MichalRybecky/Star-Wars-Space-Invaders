"""
Database handler for a CSV file.

CSV file format:
date,playtime,score,wave
"""

from datetime import datetime

stat_file = "stats.txt"


def add_game(score, wave, playtime):
    date = (str(datetime.now())).split()[0]
    with open(stat_file, "a") as file:
        file.write(f"{date},{playtime},{score},{wave}\n")
