"""
This files interprets the game files. Useful to run tests on it
"""
from src.test.game_file import read_game_file
from src.game.board import Board
from src.game.entities import Queen, Monkey, GameObject, Team


def interpret_game(path):
    game_data = read_game_file(path)

    white_queen = Queen(game_data['white_queen'], Team.WHITE, monkey_stack=game_data['stack'])
    black_queen = Queen(game_data['black_queen'], Team.BLACK, monkey_stack=game_data['stack'])

    board = Board(cols=game_data['cols'], rows=game_data['rows'])
    board.add_entity(white_queen)
    board.add_entity(black_queen)

    board.draw()

    for command in game_data['moves']:
        board.play_command(command)

    return board
