from src.game.entities import Team
from src.game.geo import Vec2I
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

    :param last_move: a list of two tuples [(x_from, y_from), (x_to, y_to)] of your opponent's last move. None if you
    are doing the first game move.

    :return: two objects Vec2I, Vec2I. The first object is the position of the piece you want to move, the second
    """

    # a list containing all the entities from all the teams (either Monkeys or Queens)
    entities = board.get_entities()

    # just like entities, but into a map. The key is a Vec2I object containing the position where you
    # want to get the entity. Use entity_map.get(Vec2I(x, y)) instead of entity_map[Vec2I(x, y)] if you want to avoid
    # raising a KeyError.
    entity_map = board.get_entity_map()

    # You can get other information from the board functions.
    your_queen = board.search_queen(your_team)

    # There are only two teams, either Team.WHITE or Team.BLACK
    enemy_team = None
    if your_team == Team.WHITE:
        enemy_team = Team.BLACK
    else:
        enemy_team = Team.WHITE

    enemy_queen = board.search_queen(enemy_team)

    # Get the position of an entity, for example, with this queen
    your_queen_position = enemy_queen.get_pos()

    # Print the position information
    print(your_queen_position.x, your_queen_position.y)

    # Get all the possible moves for your queen
    possible_moves = your_queen.get_legal_moves()

    # We want to move our queen one cell down
    your_queen_x = your_queen_position.x
    your_queen_y = your_queen_position.y

    new_position = Vec2I(your_queen_x, your_queen_y + 1)

    # We check if the new position is a legal move
    if new_position in possible_moves:
        # We make this play by returning the new_position
        return your_queen_position, new_position
    else:
        new_position = random.choice(possible_moves)
        return your_queen_position, new_position
