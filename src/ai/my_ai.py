from src.game.entities import Team, Monkey, Queen
from src.game.board import Board
from src.game.geo import Vec2I
from src.game.command import Command
import random

"""
Code your AI in this file.
"""

# Define your persistent variables here


def make_play(board, your_team, last_move):
    """
    Your AI entry point. This function gets called every time your AI is asked to make a play.
    The parameters contains all the information you need to picture the game state.

    The given lists of entities, queen information, etc... are a deep copy of the current game state, so don't try
    changing values there as this won't impact the game :p

    The execution time of this function is taken into account at each move, and a time limit is given to each team.

    :param board: the whole game state

    :param your_team: your team. Either Team.WHITE or Team.BLACK

    :param last_move: a tuple of two Vec2I (Vec2I(x_from, y_from), Vec2I(x_to, y_to)) of your opponent's last move.
    None if you are doing the first game move.

    :return: two objects Vec2I, Vec2I. The first object is the position of the piece you want to move, the second
    """

    # a list containing all the entities from all the teams (either Monkeys or Queens)
    entities = board.get_entities()

    # just like entities, but into a map (dictionary). The key is a Vec2I object containing the position where you
    # want to get the entity. Use entity_map.get(Vec2I(x, y)) instead of entity_map[Vec2I(x, y)] if you want to avoid
    # raising a KeyError. Vec2I is used for the positions
    entity_map = board.get_entity_map()

    # List all the possible legal moves
    all_possible_moves = board.get_legal_moves(your_team)

    # You can iterate over all the entities like so:
    for entity in entities:
        position = entity.get_position()
        team = entity.get_team()
        print('Entity at position {}, is from team {}'.format(position, team))

    # You can get other information from the board functions.
    your_queen = board.search_queen(your_team)

    # There are only two teams, either Team.WHITE or Team.BLACK
    enemy_team = None
    if your_team == Team.WHITE:
        enemy_team = Team.BLACK
    else:
        enemy_team = Team.WHITE

    # you can do the same with this one liner
    enemy_team = Team.WHITE if your_team == Team.BLACK else Team.BLACK

    # get the enemy queen info from the board
    enemy_queen = board.search_queen(enemy_team)

    # Get the position of an entity, for example, with this queen
    # This can also work with Monkeys
    your_queen_position = enemy_queen.get_position()

    # Get the queen stack (number of remaining monkeys)
    your_queen_stack = your_queen.get_stack()

    # Print the position information, positions use the object Vec2I, defined in the file src/game/geo.py
    print(your_queen_position.x, your_queen_position.y)

    # Get all the possible moves for your queen
    possible_moves = your_queen.get_legal_moves()

    # We want to move our queen one cell down
    your_queen_x = your_queen_position.x
    your_queen_y = your_queen_position.y

    # Again, the game uses the Vec2I object for the positions
    new_position = Vec2I(your_queen_x, your_queen_y + 1)

    # As the board is a DEEP COPY of the real board, you can use it to forecast the future, for example, if you
    # want to list all your enemy moves after the move you want to select

    # As said, you have to return a tuple of Vec2I from this function, but to make a play you have to put those
    # two Vec2I in a Command object
    move_command = Command(your_queen_position, new_position)

    # Make a copy of the current game state
    current_board = board.copy_state()

    # Plays the command, now the board is just like you have played your decised move
    board.make_play(move_command)

    # Forecast all the legal moves from your opponent
    opponent_possible_responses = board.get_legal_moves()

    # We check if the new position is a legal move
    if new_position in possible_moves:
        # We make this play by returning the new_position
        return your_queen_position, new_position
    else:
        new_position = random.choice(possible_moves)
        return your_queen_position, new_position
