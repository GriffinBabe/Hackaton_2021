from src.game.entities import Team, Monkey, Queen
from src.game.board import Board
from src.game.geo import Vec2I
from src.game.command import Command
import random
from time import time
import numpy as np

"""
Code your AI in this file.
"""

# Define your persistent variables here
DEPTH = 5
EVAL_POINTS = [[10, 8, 6, 4, 4, 6, 8, 10],
               [8, 4, 4, 6, 6, 4, 4, 8],
               [6, 4, 6, 8, 8, 6, 4, 6],
               [4, 6, 8, 10, 10, 8, 6, 4],
               [4, 6, 8, 10, 10, 8, 6, 4],
               [6, 4, 6, 8, 8, 6, 4, 6],
               [8, 4, 4, 6, 6, 4, 4, 8],
               [10, 8, 6, 4, 4, 6, 8, 10]]





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
    """
    begin = time()
    np_board = board_translate(board,your_team)
    move = alpha_beta_search(np_board, your_team)
    print("Execution time: " + str(time() - begin))
    move = (Vec2I(move[0][0], move[0][1]),Vec2I(move[1][0],move[1][1]))
    return move


def utility(board, your_team):
    if type(board) == np.float64 or type(board) == int:
        return 0 if int(board) == 2 else 500
    else:
        res = 250
        for i in range(8):
            for j in range(8):
                if board[i][j]//100 == 0:
                    if board[i][j] == 1:
                        res += EVAL_POINTS[i][j]
                    elif board[i][j] == 2:
                        res -= EVAL_POINTS[i][j]
    return res


def cutoff_test(board, depth):
    return depth >= DEPTH or type(board) == float or type(board) == int


def max_value(board, your_team, alpha, beta, depth, test_move):
    if cutoff_test(board, depth):
        return utility(board, 1)
    utility_value = -100000
    for move in get_legal_moves(board, 1):
        new_board = board.copy()
        new_board = play_move(new_board, move)
        utility_value = max(utility_value, min_value(new_board, 1, alpha, beta, depth + 1, test_move))
        if utility_value >= beta or utility_value == 500:
            return utility_value
        alpha = max(alpha, utility_value)
    return utility_value


def min_value(board, your_team, alpha, beta, depth, test_move):
    if cutoff_test(board, depth):
        return utility(board, 1)
    utility_value = 100000
    for move in get_legal_moves(board, 2):
        new_board = board.copy()
        new_board = play_move(new_board, move)
        utility_value = min(utility_value, max_value(new_board, 1, alpha, beta, depth + 1, test_move))
        beta = min(beta, utility_value)
        if utility_value <= alpha or utility_value == 0:
            return utility_value
    return utility_value


def alpha_beta_search(board, your_team):
    depth = 1
    alpha = -100000
    beta = 100000
    next_move = ((0, 0), (0, 0))
    for move in get_legal_moves(board, 1):
        new_board = board.copy()
        new_board = play_move(new_board, move)
        utility_value = min_value(new_board, 1, alpha, beta, depth + 1, move)
        if utility_value > alpha:
            next_move = move
        alpha = max(alpha, utility_value)
    return next_move


def board_translate(board, your_team):
    n_board = np.zeros((8, 8))
    board_map = board.get_entity_map()
    for pos in board_map:
        if board_map[pos].is_queen():
            team = 100 if board_map[pos].get_team() == your_team else 200
            n_board[pos.x, pos.y] = team + board_map[pos].get_stack()
        else:
            n_board[pos.x, pos.y] = 1 if board_map[pos].get_team() == your_team else 2
    return n_board


def play_move(board, command):
    pos_from = command[0]
    pos_to = command[1]
    # legal_moves = get_legal_moves(board, team)
    if board[pos_to] // 100 > 0:
        return int(board[pos_from] // 100)
    else:
        if board[pos_from] // 100 > 0 and board[pos_to] == 0 and board[pos_from] % 100 > 0:
            piece_from = board[pos_from] - 1
            board[pos_to] = piece_from
            board[pos_from] = board[pos_from] // 100
        else:
            piece_from = board[pos_from]
            board[pos_to] = piece_from
            board[pos_from] = 0
    return board


def get_legal_moves(board, team):
    legal_moves = [[],[]]
    for i in range(8):
        for j in range(8):
            positions = []
            if board[i, j] == team:
                positions = monkey_moves(board, (i, j))
            elif board[i, j] > 3 and board[i, j]//100 == team:
                positions = queen_moves(board, (i, j))
            for k in range(2):
                if positions:
                    for pos in positions[k]:
                        if pos != (i, j):
                            legal_moves[k].append(((i, j), pos))
    final_legal_positions = legal_moves[0]+legal_moves[1]
    return final_legal_positions
    #[[(1,2),(1,0)],[(3,2),(1,0)]] #n n+1


def monkey_moves(board, pos):
    team = board[pos] // 100 if board[pos] // 100 != 0 else board[pos]
    enemy_queen = search_enemy_queen(board, team)
    legal_positions = get_legal_positions(board, pos)
    # Check if the new moves makes us closed from the queen
    dist_vec = np.array((pos[0]-enemy_queen[0], pos[1]-enemy_queen[1]))
    pos_queen_distance = np.linalg.norm(dist_vec)
    final_legal_positions = [[], []]
    for i in range(2):
        for new_pos in legal_positions[i]:
            dist_vec = np.array((new_pos[0] - enemy_queen[0], new_pos[1] - enemy_queen[1]))
            new_distance = np.linalg.norm(dist_vec)
            if new_distance < pos_queen_distance:
                final_legal_positions[i].append(new_pos)
    return final_legal_positions


def queen_moves(board, position):
    team = board[position] // 100 if board[position] // 100 != 0 else board[position]
    enemy_team = 1 if team != 1 else 2
    legal_positions = get_legal_positions(board, position)
    final_legal_positions = [[],[]]
    for i in range(2):
        for new_pos in legal_positions[i]:
            legal = True
            if not board[new_pos] >= 100:
                for shift_x, shift_y in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    pos = new_pos
                    pos = (pos[0]+shift_x, pos[1]+shift_y)
                    while check_boundaries(pos):
                        if board[pos] == enemy_team or board[pos]//100 == enemy_team:
                            legal = False
                            break
                        pos = (pos[0] + shift_x, pos[1] + shift_y)
                    if not legal:
                        break
            if legal:
                final_legal_positions[i].append(new_pos)

    return final_legal_positions


def check_boundaries(pos):
    return 8 > pos[0] >= 0 and 8 > pos[1] >= 0


def get_legal_positions(board, position):
    a_legal_positions = []
    n_legal_positions = []
    team = board[position]//100 if board[position]//100 != 0 else board[position]
    for shift_x, shift_y in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        pos = position
        pos = (pos[0]+shift_x, pos[1]+shift_y)
        while check_boundaries(pos):
            if board[pos] == 0:
                n_legal_positions.append(pos)
                pos = (pos[0] + shift_x, pos[1] + shift_y)
            else:
                if (board[pos] != team and board[pos] < 3) or (board[pos]//100 != team and board[pos]//100 != 0):
                    a_legal_positions.append(pos)
                break
    return [a_legal_positions, n_legal_positions]


def search_enemy_queen(board, team):
    enemy_team = 1 if team != 1 else 2
    for i in range(8):
        for j in range(8):
            if board[i, j]//100 == enemy_team:
                return i, j
