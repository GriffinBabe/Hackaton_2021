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
import json
import random
import itertools
import datetime
import signal
from importlib import import_module
from src.game.board import Board
from src.game.entities import Team, Queen
from src.game.geo import Vec2I
from src.game.command import Command


class TimeOutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeOutException


def write_json(dict, path):
    """
    Writes dictionary content into a json file
    """
    with open(path, 'w') as outfile:
        json.dump(dict, outfile)


def load_function(path):
    """
    Dynamically loads a module from a python file, and returns the make_play function.
    """
    module_path = path.replace('./', '').replace('/', '.').replace('\\', '.')
    module = import_module(module_path)
    function = getattr(module, 'make_play')
    return function


def load_pools(path):
    """
    Returns a list of lists containing the team names
    :param path: Path of pools.json
    :return: a list of lists
    """
    data = []
    with open(path) as json_file:
        pool_data = json.load(json_file)
        for pool in pool_data['pools']:
            pool_names = []
            for team in pool['teams']:
                pool_names.append(team)
            data.append(pool_names)
    return data


def test_existing_script(team_dir_path, team_names):
    """
    Checks if all the teams have the file my_ai.py ready
    :param team_dir_path: the dir where there are all the team folders
    :param team_names: a list of all the teams to check
    :return: True if all good, false otherwise
    """
    for name in team_names:
        full_path = os.path.join(team_dir_path, name, 'my_ai')
        try:
            fun = load_function(full_path)
            print('Found function for team: {}'.format(name))
        except Exception as e:
            print(e)
            return False
    return True


def load_game():
    game = Board(cols=8, rows=8)
    white_queen = Queen(Vec2I(3, 0), Team.WHITE, monkey_stack=12)
    black_queen = Queen(Vec2I(4, 7), Team.BLACK, monkey_stack=12)
    game.add_entity(white_queen)
    game.add_entity(black_queen)
    return game


# noinspection DuplicatedCode
def play_match(white_team, black_team, white_team_path, black_team_path):
    print('\033[1;36;40m Starting match {} vs {} \033[1;33;40m'.format(white_team, black_team))
    date = datetime.datetime.now()

    dict = {}
    dict['date'] = date.strftime('%d/%m/%Y %H:%M:%S')
    dict['white_team'] = white_team
    dict['black_team'] = black_team
    dict['stack'] = 12
    dict['cols'] = 8
    dict['rows'] = 8
    dict['white_queen'] = '3, 0'
    dict['black_queen'] = '4, 7'

    moves = []

    last_move = None

    winner = None

    reason = 'None'

    white_remaining_time_ms = 4 * 60 * 1000  # 3 minutes
    black_remaining_time_ms = 4 * 60 * 1000  # 3 minutes

    white_team_function = load_function(white_team_path)
    black_team_function = load_function(black_team_path)

    board = load_game()

    signal.signal(signal.SIGALRM, timeout_handler)

    while board.get_winner() is None:

        if len(board.get_legal_moves()) == 0:
            winner = Team.WHITE if board.get_turn() == Team.BLACK else Team.BLACK
            reason = 'out of legal moves'
            print('\033[1;31;40m Game over. {} is out of legal moves.\033[1;37;40m'.format('black' if winner == Team.WHITE else 'white'))
            break

        board_copy = board.copy_state()
        start = datetime.datetime.now()

        if board.get_turn() == Team.WHITE:
            try:
                print('\033[1;32;40m White to play \033[1;37;40m')
                signal.alarm(int(white_remaining_time_ms / 1000))
                play = white_team_function(board_copy, Team.WHITE, last_move)
                signal.alarm(0)
                last_move = play

                end = datetime.datetime.now()
                diff = int((end - start).seconds * 1000)
                white_remaining_time_ms -= diff

                command = Command(play[0], play[1])
                board.play_command(command)
                moves.append('({}, {} -> {}, {})'.format(play[0].x, play[0].y, play[1].x, play[1].y))
            except TimeOutException as tout:
                print('\033[1;31;40m Team {} timed out, dropping the game.\033[1;37;40m'.format(white_team))
                reason = 'timeout'
                winner = Team.BLACK
                break
            except Exception as e:
                print('\033[1;31;40m Team: {} got exception: {}, dropping the game\033[1;37;40m'.format(white_team, e))
                reason = 'exception'
                winner = Team.BLACK
                break
        else:
            try:
                print('\033[1;32;40m Black to play \033[1;37;40m')
                signal.alarm(int(black_remaining_time_ms / 1000))
                play = black_team_function(board_copy, Team.BLACK, last_move)
                signal.alarm(0)
                last_move = play

                end = datetime.datetime.now()
                diff = int((end - start).seconds * 1000)
                black_remaining_time_ms -= diff

                command = Command(play[0], play[1])
                board.play_command(command)
                moves.append('({}, {} -> {}, {})'.format(play[0].x, play[0].y, play[1].x, play[1].y))
            except TimeOutException as tout:
                print('\033[1;31;40m Team {} timed out, dropping the game.\033[1;37;40m'.format(black_team))
                reason = 'timeout'
                winner = Team.WHITE
                break
            except Exception as e:
                print('\033[1;31;40m Team: {} got exception: {}, dropping the game\033[1;37;40m'.format(black_team, e))
                reason = 'exception'
                winner = Team.WHITE
                break

        print('Move player: {} from team {}. White time: {} Black time: {}'
              .format(last_move,
                      'white' if board.get_turn() == Team.BLACK else 'black',
                      white_remaining_time_ms,
                      black_remaining_time_ms))

    if winner is None:
        print("\033[1;31;40mQueen captured!\033[1;37;40m")
        winner = board.get_winner()
        reason = 'queen captured'

    print('\033[1;31;40m Match {} vs {}, team {} wins\033[1;37;40m'.format(white_team, black_team, white_team if winner == Team.WHITE else black_team))
    dict['winner'] = 'white' if winner == Team.WHITE else 'black'
    dict['white_remaining_time'] = white_remaining_time_ms
    dict['black_remaining_time'] = black_remaining_time_ms
    dict['moves'] = moves
    dict['reason'] = reason

    return dict


def play_pool(teams, pool_number, game_path, teams_path):
    pool_path = os.path.join(game_path, str(pool_number))
    match_combinations = list(itertools.combinations(teams, 2))
    for number, teams in enumerate(match_combinations):
        teams = list(teams)
        random.shuffle(teams)
        team_0_path = os.path.join(teams_path, teams[0], 'my_ai')
        team_1_path = os.path.join(teams_path, teams[1], 'my_ai')
        game_data = play_match(team_0_path, team_1_path, teams[0], teams[1])
        write_json(game_data, os.path.join(game_path, str(pool_number), '{}_vs_{}.json'.format(teams[0], teams[1])))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception('Must specify two paths.')

    team_folder = sys.argv[1]
    game_folder = sys.argv[2]

    pool_file_path = os.path.join(team_folder, 'pools.json')
    pools = load_pools(pool_file_path)

    assert test_existing_script(team_folder, [item for sublist in pools for item in sublist])

    for idx, pool in enumerate(pools):
        play_pool(pool, idx + 1, game_folder, team_folder)
