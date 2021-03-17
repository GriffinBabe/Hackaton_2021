"""
Benchmarking tool, this will load and test each team against each other.

Teams must be formatted into a directory, for example

- Teams:
    - team_name_1:
        - my_ai.py
    - team_name_2:
        - my_ai.py
    - team_name_3:
        - my_ai.py

- Games:
    - name_1_vs_name_2_1.json
    - name_1_vs_name_2_2.json
    - name_1_vs_name_2_3.json
    - etc

All the games will be saved as json files.
"""

import os
import sys
from importlib import import_module
from src.game.board import Board
from src.game.entities import Team, Queen
from src.game.geo import Vec2I


def load_function(path):
    module = import_module(path)
    function = getattr(module, 'make_play')
    print(function)
    return function


def load_game():
    game = Board(cols=8, rows=8)
    white_queen = Queen(Vec2I(3, 0), Team.WHITE, monkey_stack=12)
    black_queen = Queen(Vec2I(4, 7), Team.BLACK, monkey_stack=12)
    game.add_entity(white_queen)
    game.add_entity(black_queen)
    return game


def match_teams(team_1, team_2, team_folder, game_folder):
    team_1_script = os.path.join(team_folder, team_1, 'my_ai').replace('/', '.').replace('\\', '.')
    team_2_script = os.path.join(team_folder, team_2, 'my_ai').replace('/', '.').replace('\\', '.')
    game = load_game()

    team_1_function = load_function(team_1_script)
    team_2_function = load_function(team_2_script)

    while game.get_winner() is None:
        pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception('Must specify two paths.')

    team_folder = sys.argv[1]
    game_folder = sys.argv[2]

    teams = os.listdir(team_folder)

    for team_1 in teams:
        for team_2 in teams:
            if team_1 != team_2:
                match_teams(team_1, team_2, team_folder, game_folder)


