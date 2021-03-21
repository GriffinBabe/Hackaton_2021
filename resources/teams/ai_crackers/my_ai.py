from src.game.entities import Team, Monkey, Queen
from src.game.board import Board
from src.game.geo import Vec2I
from src.game.command import Command
import random
import numpy as np

"""
Code your AI in this file.
"""

# Define your persistent variables here
MAX_DEPTH = 3
my_moves = []
adv_moves = []


def make_play(board, your_team, last_move):
    move = min_max(board, 0, your_team)
    return move[1]


def min_max(board, depth, team):

    if depth >= MAX_DEPTH:
        h = heuristic(board, team)
        return [h, None]
    moves = []

    for move in remove_bad_moves(board):  # changer de player une fois sur deux
        current_board = board.copy_state()
        current_board.play_command(Command(move[0], move[1]))
        if current_board.get_winner() is None:
            pass
        elif current_board.get_winner() == team:
            return [1000, move]
        else:
            return [-10000, move]
        m = min_max(current_board, depth + 1, team)
        m[1] = move
        moves.append(m)

    if depth % 2 == 0:
        move1 = [test[0] for test in moves]
        selection = []
        for i, e in enumerate(move1):
            if e == max(move1):
                selection.append(i)
        move = moves[random.choice(selection)]
    else:
        move1 = [test[0] for test in moves]
        selection = []
        for i, e in enumerate(move1):
            if e == min(move1):
                selection.append(i)
        move = moves[random.choice(selection)]
    return move


def heuristic(board, team):
    h = 0
    my_entities = 0
    adv_entities = 0
    my_cover = 0
    adv_cover = 0
    global my_moves
    global adv_moves
    enemy_team = Team.WHITE if team == Team.BLACK else Team.BLACK
    queen = board.search_queen(team)
    stack = queen.get_stack()
    adv_stack = board.search_queen(enemy_team).get_stack()
    adv_atk = [elem[1] for elem in adv_moves]
    my_atk = [elem[1] for elem in my_moves]
    for entity in board.get_entities():
        if entity.get_team() == team:
            my_cover += [elem[0] for elem in my_moves].count(entity.get_position())
            if entity.get_position() in adv_atk:
                if entity.is_queen():
                    h -= 10000
                else:
                    h -= adv_atk.count(entity.get_position())
        elif entity.get_team() == enemy_team:
            adv_entities += 1
            adv_cover -= [elem[0] for elem in adv_moves].count(entity.get_position())
            if entity.get_position() in my_atk:
                if entity.is_queen():
                    h += 15
                else:
                    h += (2 * my_atk.count(entity.get_position()))
    h += (my_entities * my_entities - adv_entities * adv_entities + my_cover//2 - adv_cover//2 - stack + adv_stack)
    return h


def remove_bad_moves(board):
    my_team = board.get_turn()
    enemy_team = Team.WHITE if my_team == Team.BLACK else Team.BLACK
    global my_moves
    my_moves = board.get_legal_moves(my_team)
    global adv_moves
    adv_moves = board.get_legal_moves(enemy_team)
    lst = []
    lst1 = []

    for elem in adv_moves:
        lst.append(elem[1])
    for elem in my_moves:
        if elem[1] not in lst:
            lst1.append(elem)
        elif elem[0] != board.search_queen(my_team).get_position():
            if random.randint(0, 10) < 2:
                lst1.append(elem)
    if len(lst1) == 0:
        lst1 = my_moves
    return lst1
