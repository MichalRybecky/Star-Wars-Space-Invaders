"""
Module that handles creating and returning game leaderboard

CSV file format:
date,playtime,score,wave
"""


def get_games() -> list:
    """
    returns all games in a list from a CSV file in correct type
    """
    with open("stats.txt") as file:
        games_from_file = [game.strip().split(",") for game in file.readlines()]

    games = []
    for game in games_from_file:
        date = game[0]
        playtime = int(game[1])
        score = int(game[2])
        wave = int(game[3])
        games.append([date, playtime, score, wave])
    return games


def sort_on_date(games) -> list:
    """
    sorts games from newest to oldest
    """
    pass


def sort_on_type(games, sort_type) -> list:
    """
    sorts games based on type parameter, which are identical to create_leaderboad types except 'date'
    """
    sort_types = {"playtime": 1, "score": 2, "wave": 3}
    sorted_list = sorted(games, key=lambda x: x[sort_types[sort_type]], reverse=True)
    return sorted_list


def create_leaderboard(sort_type="score") -> list:
    """
    creates leaderboard based on the parameter, which can be:
    'date' for newest to oldest,
    'playtime' for highest to lowest playtime,
    'score' for highest to lowest score,
    'wave' for highest to lowest wave
    """
    games = get_games()
    if sort_type == 'date':
        print('This function is not supported yet.')
        return

    return sort_on_type(games, sort_type)
