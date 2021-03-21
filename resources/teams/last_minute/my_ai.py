import time

from src.game.entities import Team, Monkey, Queen
from src.game.board import Board
from src.game.geo import Vec2I
from src.game.command import Command
import random

"""
Code your AI in this file.
"""

# Define your persistent variables here

depth = 2
infinity = 10000
alpha = -infinity
beta = infinity
time_limit = 10
turn = 0

tier_1 = [Vec2I(3, 3), Vec2I(3, 4), Vec2I(4, 3), Vec2I(4, 4)]
tier_2 = [Vec2I(2, 2), Vec2I(3, 2), Vec2I(4, 2), Vec2I(5, 2),
          Vec2I(5, 3), Vec2I(5, 4), Vec2I(5, 5), Vec2I(4, 5),
          Vec2I(3, 5), Vec2I(2, 5), Vec2I(2, 4), Vec2I(2, 3)]


def make_play(board, your_team, last_move):

    global turn

    all_moves = board.get_legal_moves(your_team)
    all_final_positions = [move[1] for move in all_moves]
    all_double_moves = []
    random.shuffle(all_moves)

    for final_position in all_final_positions:
        if all_final_positions.count(final_position) >= 2:
            all_double_moves.append(final_position)

    enemy_positions, enemy_moves = [], []
    for move in board.get_legal_moves(enemy_moves):
        enemy_positions.append(move[0])
        enemy_moves.append(move[1])

    enemy_team = Team.WHITE if your_team == Team.BLACK else Team.BLACK
    queen_in_danger = False
    for move in board.get_legal_moves(enemy_team):
        if move[1] == board.search_queen(your_team).get_position():
            queen_in_danger = True
            break

    queen_moves = []
    for move in all_moves:  # lists all queen moves that don't immediately put her in danger
        if move[0] == board.search_queen(your_team).get_position():
            if move[1] in enemy_moves:  # removes all moves putting the queen in the line of fire
                all_moves.pop(all_moves.index(move))
            else:
                queen_moves.append(move)

    if turn < 2:
        for move in all_moves:  # checks all moves in the outer center circle
            if move[1] in tier_2:
                all_moves.insert(0, all_moves.pop(all_moves.index(move)))

        for move in all_moves:  # checks all moves in the inner center circle
            if move[1] in tier_1:
                all_moves.insert(0, all_moves.pop(all_moves.index(move)))

    if queen_in_danger:  # if queen is in danger, checks all possible queen moves first
        for move in queen_moves:
            all_moves.insert(0, all_moves.pop(all_moves.index(move)))

    for move in all_moves:
        if move[1] in all_double_moves:
            all_moves.insert(0, all_moves.pop(all_moves.index(move)))

    for move in all_moves:  # checks all moves capable of capturing enemy monkeys
        if move[1] in enemy_positions:
            all_moves.insert(0, all_moves.pop(all_moves.index(move)))

    for move in all_moves:  # checks all moves on an enemy path LAST
        if move[1] in enemy_moves:
            all_moves.append(all_moves.pop(all_moves.index(move)))

    best_move = all_moves[0]
    init_time = time.time()

    if your_team == Team.WHITE:
        best_val = -infinity
        for current_move in all_moves:
            new_board = board.copy_state()
            new_board.play_command(Command(current_move[0], current_move[1]))
            val = minimax(new_board, depth, alpha, beta, False)
            if val > best_val:
                best_val = val
                best_move = current_move
            curr_time = time.time()
            print(curr_time - init_time)
            if curr_time - init_time > time_limit:
                break

    else:
        best_val = +infinity
        for current_move in all_moves:
            new_board = board.copy_state()
            new_board.play_command(Command(current_move[0], current_move[1]))
            val = minimax(new_board, depth, alpha, beta, True)
            if val < best_val:
                best_val = val
                best_move = current_move
            curr_time = time.time()
            print(curr_time - init_time)
            if curr_time - init_time > time_limit:
                break

    turn += 1

    return best_move


def eval_func(new_board):
    score = 0

    white_baby_positions = []
    white_baby_moves = []
    white_queen_position = new_board.search_queen(Team.WHITE).get_position()
    white_queen_moves = []

    for move in new_board.get_legal_moves(Team.WHITE):
        if move[0] == white_queen_position:
            white_queen_moves.append(move[1])
        else:
            white_baby_positions.append(move[0])
            white_baby_moves.append(move[1])

    black_baby_positions = []
    black_baby_moves = []
    black_queen_position = new_board.search_queen(Team.BLACK).get_position()
    black_queen_moves = []

    for move in new_board.get_legal_moves(Team.BLACK):
        if move[0] == black_queen_position:
            black_queen_moves.append(move[1])
        else:
            black_baby_positions.append(move[0])
            black_baby_moves.append(move[1])


    white_baby_positions = list(dict.fromkeys(white_baby_positions))
    white_baby_moves = list(dict.fromkeys(white_baby_moves))

    black_baby_positions = list(dict.fromkeys(black_baby_positions))
    black_baby_moves = list(dict.fromkeys(black_baby_moves))

    white_positions = [white_queen_position] + white_baby_positions
    black_positions = [black_queen_position] + black_baby_positions

    white_moves = white_baby_moves + white_queen_moves
    black_moves = black_baby_moves + black_queen_moves

    if white_queen_position in black_moves:
        score -= 256
    elif black_queen_position in white_moves:
        score += 256
    else:

        score += len(white_baby_positions) * 32
        score -= len(black_baby_positions) * 32

        score += len(white_moves)
        score -= len(black_moves)

        for position in white_positions:
            if position in black_moves:
                score -= 8

        for position in black_positions:
            if position in white_moves:
                score += 8

    if new_board.get_winner() == Team.WHITE:
        score += 512
    elif new_board.get_winner() == Team.BLACK:
        score -= 512

    return score


def endgame(board):
    return board.get_winner() is not None


def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or endgame(board):
        return eval_func(board)

    if maximizingPlayer:
        max_eval = -infinity
        all_moves = board.get_legal_moves(Team.WHITE)
        random.shuffle(all_moves)
        for current_move in all_moves:
            new_board = board.copy_state()
            new_board.play_command(Command(current_move[0], current_move[1]))
            eval = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = +infinity
        all_moves = board.get_legal_moves(Team.BLACK)
        random.shuffle(all_moves)
        for current_move in all_moves:
            new_board = board.copy_state()
            new_board.play_command(Command(current_move[0], current_move[1]))
            eval = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
