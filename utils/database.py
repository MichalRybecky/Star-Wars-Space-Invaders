"""
Database handler for a CSV file.

CSV file format:
date,daytime,score,wave
"""

from datetime import datetime

stat_file = 'stats.txt'


def add_game(score, wave):
    naive_time = str(datetime.now())
    date, time = naive_time.split()
    time = time.split('.')
    with open(stat_file, 'a') as file:
        file.write(f'{date},{time[0]},{score},{wave}\n')


