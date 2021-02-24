"""
This file contains all the necessary tools to interpret command from files
"""
import json
import datetime
from src.game.geo import Vec2I
from src.game.command import Command


def read_game_file(path):
    """
    Reads a JSON game file and returns a board with a list of command to interpret.

    Example of a very low rating game file:

    {
      "date": "24/02/2021 11:45:20",
      "cols": 8,
      "rows": 8,
      "stack": 8,
      "white_queen": "4, 1",
      "black_queen": "5, 8",
      "moves": ["4, 1 -> 4, 8", "5, 8 -> 4, 8"]
    }

    :param path: The path to the file
    :return: A dictionary containing the date, width, height, stack, white_queen, black_queen and moves positions
    encoded in the game's classes
    """
    data_formatted = {}
    with open(path, 'r') as infile:
        data = json.load(infile)

        data_formatted['cols'] = data['cols']
        data_formatted['rows'] = data['rows']
        data_formatted['stack'] = data['stack']

        white_queen = data['white_queen'].split(', ')
        black_queen = data['black_queen'].split(', ')

        data_formatted['white_queen'] = Vec2I.parse_from_list(white_queen)
        data_formatted['black_queen'] = Vec2I.parse_from_list(black_queen)

        date_str = data.get('date')
        if date_str is not None:
            date = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
            data_formatted['date'] = date

        command_list = []
        moves_str = data['moves']
        for move in moves_str:
            move_split = move.split(' -> ')
            move_from_str = move_split[0].split(', ')
            move_to_str = move_split[1].split(', ')
            move_from = Vec2I.parse_from_list(move_from_str)
            move_to = Vec2I.parse_from_list(move_to_str)
            command = Command(move_from, move_to)
            command_list.append(command)

        data_formatted['moves'] = command_list

        return data_formatted
