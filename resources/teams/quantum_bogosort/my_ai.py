import random
import numpy as np
from src.game.entities import Team, Monkey, Queen
from src.game.command import Command


def get_ennemy_team(your_team):
    return Team.WHITE if your_team == Team.BLACK else Team.BLACK


def distFromCorner(i, j):
    return np.sqrt((i - 3.5)**2 + (j - 3.5)**2) / (4 * 2**0.5)


QUEEN_TABLE = (40 + np.array([
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10,   0,   5,  0,  0,   0,   0, -10],
    [-10,   5,   5,  5,  5,   5,   0, -10],
    [0,   0,   5,  5,  5,   5,   0,  -5],
    [-5,   0,   5,  5,  5,   5,   0,  -5],
    [-10,   0,   5,  5,  5,   5,   0, -10],
    [-10,   0,   0,  0,  0,   0,   0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
])) / 45

QUEEN_TABLE_MEAN = np.mean(QUEEN_TABLE)


def board_code_fast(board, team, white_stack, black_stack):
    code = ['White' if team == Team.WHITE else 'Black']
    code.append('J' + str(white_stack))
    code.append('K' + str(black_stack))
    for index in range(64):
        i = index // 8
        j = index % 8
        if board[i, j] == 1:
            code.append('w' + str(i) + str(j))
        elif board[i, j] == -1:
            code.append('b' + str(i) + str(j))
        elif board[i, j] == 2:
            code.append('W' + str(i) + str(j))
        elif board[i, j] == -2:
            code.append('B' + str(i) + str(j))
    code.sort()
    return ''.join(code)


def scanBoard(board, team):
    # 1 -> monckey blanc
    # 2 -> reine blanche
    # -1 -2 noire
    board = np.copy(board)

    if team == Team.BLACK:
        board = board * -1

    queen_i = 0
    queen_j = 0

    poss_move = []

    list_pos = []

    score = 0
    tot_score = 0

    for index in range(64):
        i = index // 8
        j = index % 8

        score += board[i, j] * QUEEN_TABLE[i, j]
        tot_score += np.abs(board[i, j] * QUEEN_TABLE[i, j])

        if board[i, j] > 0:
            list_pos.append((i, j))

        if board[i, j] == -2:
            queen_i = i
            queen_j = j

    target_queen = False

    for i, j in list_pos:
        for dx, dy in ((0, 1), (1, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)):
            di = dx
            dj = dy
            if board[i, j] == 2:
                while i + di < 8 and j + dj < 8 and i + di >= 0 and j + dj >= 0 and board[i + di, j + dj] == 0:
                    poss_move.append((((i, j), (i + di, j + dj)), False))
                    di += dx
                    dj += dy
                if i + di < 8 and j + dj < 8 and i + di >= 0 and j + dj >= 0 and board[i + di, j + dj] < 0:
                    poss_move.append((((i, j), (i + di, j + dj)), True))
                    if board[i + di, j + dj] == -2:
                        target_queen = True
            else:
                current_dist = (i - queen_i)**2 + (j - queen_j)**2
                while i + di < 8 and j + dj < 8 and i + di >= 0 and j + dj >= 0 and (i + di - queen_i)**2 + (j + dj - queen_j)**2 < current_dist and board[i + di, j + dj] == 0:
                    poss_move.append((((i, j), (i + di, j + dj)), False))
                    di += dx
                    dj += dy
                if i + di < 8 and j + dj < 8 and i + di >= 0 and j + dj >= 0 and (i + di - queen_i)**2 + (j + dj - queen_j)**2 < current_dist and board[i + di, j + dj] < 0:
                    poss_move.append((((i, j), (i + di, j + dj)), True))
                    if board[i + di, j + dj] == -2:
                        target_queen = True

    return poss_move, target_queen, score, tot_score


def playCommand(board_state, command, team):
    f, to = command
    fx, fy = f
    tox, toy = to

    boards, stack_blanc, stack_noir = board_state
    boards = np.copy(boards)

    stack_current = stack_blanc if Team.WHITE == team else stack_noir

    boards[tox, toy] = boards[fx, fy]

    if np.abs(boards[tox, toy]) == 1:
        boards[fx, fy] = 0
    elif stack_current > 0:
        stack_current -= 1
        boards[fx, fy] = np.sign(boards[fx, fy])

    return (boards, stack_current if Team.WHITE == team else stack_blanc,
            stack_current if Team.BLACK == team else stack_noir)


DP_white, DP_black = {}, {}

# team vient de jouer


def minimax_alpha_beta(board_state, team, your_team, depht, leafs_explored,  alpha=1, beta=1):

    global DP_white, DP_black

    DP = DP_white if your_team == Team.WHITE else DP_black

    ennemy_team = get_ennemy_team(team)
    boards, stack_blanc, stack_noir = board_state

    code = board_code_fast(boards, team, stack_blanc, stack_noir)
    if code in DP:
        return DP[code]

    stack_values = 0.8 * (stack_blanc - stack_noir) * QUEEN_TABLE_MEAN
    tot_stack_value = 0.8 * (stack_blanc + stack_noir) * QUEEN_TABLE_MEAN

    if Team.BLACK == your_team:
        stack_values *= -1

    leafs_explored[0] += 1

    all_possible_moves, target_queen, value_eval, value_tot_eval = scanBoard(
        boards, ennemy_team)

    if ennemy_team != your_team:
        value_eval *= -1

    values = -1e9 if team != your_team else 1e9

    if target_queen:
        DP[code] = (-1e9 if team == your_team else 1e9) + (value_eval + stack_values) / \
            (value_tot_eval + tot_stack_value)
        return DP[code]

    all_possible_moves.sort(key=lambda x: x[1], reverse=True)

    if depht == 0:
        values = (value_eval + stack_values) / \
            (value_tot_eval + tot_stack_value)

    for command, capture in all_possible_moves:
        new_board_state = playCommand(board_state, command, team)
        if team != your_team:
            if depht != 0:
                values = max(values, minimax_alpha_beta(new_board_state,
                                                        ennemy_team, your_team, depht - 1, leafs_explored, alpha, beta))

            elif capture:
                values = max(values, minimax_alpha_beta(new_board_state,
                                                        ennemy_team, your_team, 0, leafs_explored, alpha, beta))
            alpha = max(alpha, values)
            if alpha >= beta:
                break
        else:
            if depht != 0:
                values = min(values, minimax_alpha_beta(new_board_state,
                                                        ennemy_team, your_team, depht - 1, leafs_explored, alpha, beta))

            elif capture:
                values = min(values, minimax_alpha_beta(new_board_state,
                                                        ennemy_team, your_team, 0, leafs_explored, alpha, beta))
            beta = min(beta, values)
            if alpha >= beta:
                break

    DP[code] = values
    return DP[code]


def convert_board(board):
    fast_board = np.zeros((8, 8), dtype=int)

    stack_blanc = 0
    stack_noir = 0

    for e in board.get_entities():
        i = e.get_position().x
        j = e.get_position().y

        if e.get_team() == Team.WHITE:
            if e.is_queen():
                fast_board[i, j] = 2
                stack_blanc = e.get_stack()
            else:
                fast_board[i, j] = 1
        else:
            if e.is_queen():
                stack_noir = e.get_stack()
                fast_board[i, j] = -2
            else:
                fast_board[i, j] = -1
    return (fast_board, stack_blanc, stack_noir)


def make_play(board, your_team, last_move):
    """
    Example of a very stupid AI. Don't do this at home.
    """
    global DP_white, DP_black

    all_moves = board.get_legal_moves(your_team)
    queen_ennemy_pos = board.search_queen(
        get_ennemy_team(your_team)).get_position()

    values = -1e10
    poss_move = []

    leafs_explored = [0]
    for possible_move in all_moves:
        f, to = possible_move
        x = to.x
        y = to.y
        if x == queen_ennemy_pos.x and y == queen_ennemy_pos.y:
            # print('CAPTURE')
            return possible_move
        else:
            current_board = board.copy_state()
            current_board.play_command(Command(f, to))

            v = minimax_alpha_beta(convert_board(
                current_board), your_team, your_team, 1, leafs_explored, alpha=-1e9, beta=1e9)

            # print(v)

            if v > values:
                poss_move = [possible_move]
                values = v
            elif v == values:
                poss_move.append(possible_move)

        # print(len(DP_white))

    choice = random.choice(poss_move)
    print('SCORE  : ', values)
    print(your_team, 'MOVE', choice, 'LEAFS = ', leafs_explored[0])
    return choice
