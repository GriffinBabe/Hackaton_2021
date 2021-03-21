from src.game.entities import Team, Monkey, Queen
from src.game.board import Board
from src.game.geo import Vec2I
from src.game.command import Command
import math
import random
import concurrent.futures

"""
Code your AI in this file.
"""

# Define your persistent variables here

def print_board(board):
    map = board.get_entity_map()	
    grid = [['.' for j in range(8)] for i in range(8)]
    for key in map:
        if map[key].is_queen():
            char = 'Q'
        else:
            char = 'M'
        if map[key].get_team() == Team.BLACK:
            char = char.lower()
        grid[key.y][key.x] = char
    for i in range(8):
        print(*grid[i], sep=' ')


def minimax(board, your_team, enemy_team, max_depth, part, cut, root_move=None, score=0, depth=0, alpha=(-math.inf, None), beta=(math.inf, None), maximizingPlayer=True):
    if depth == max_depth:
        answer = (score, root_move)

    elif maximizingPlayer: 
        maxEval = (-math.inf, root_move)
        pruning = False
        moves = board.get_legal_moves(your_team)
        if depth == 0:
            moves = moves[round(len(moves)/cut*part):round(len(moves)/cut*(part+1))]
        i = 0
        while i < len(moves) and not pruning:
            if depth == 0:
                root_move = moves[i]
            map = board.get_entity_map()	

            sourceMove = Vec2I(moves[i][0].x, moves[i][0].y)
            targetMove = Vec2I(moves[i][1].x, moves[i][1].y)
            sourcePawn = map.get(sourceMove)
            targetPawn = map.get(targetMove)
            value = 0
            if targetPawn:
                if targetPawn.is_queen():
                    return (math.inf, root_move)
                else:
                    value += 1
            if sourcePawn:
                if sourcePawn.is_queen():
                    if not targetPawn:
                        value += 0.6
            new_move = Command(moves[i][0], moves[i][1])
            new_board = board.copy_state()
            new_board.play_command(new_move)
            evaluation = minimax(new_board, your_team, enemy_team, max_depth, part, cut, root_move, score + value, depth + 1, alpha, beta, False)
            if maxEval[0] != evaluation[0]:
                maxEval = max(maxEval, evaluation)
            if alpha[0] != evaluation[0]:
                alpha = max(alpha, evaluation)
            if beta[0] <= alpha[0]:
                pruning = True
            i = i + 1
        answer = maxEval

    else:
        minEval = (math.inf, root_move)
        pruning = False
        moves = board.get_legal_moves(enemy_team)
        i = 0
        while i < len(moves) and not pruning:
            map = board.get_entity_map()	
            sourceMove = Vec2I(moves[i][0].x, moves[i][0].y)
            targetMove = Vec2I(moves[i][1].x, moves[i][1].y)
            sourcePawn = map.get(sourceMove)
            targetPawn = map.get(targetMove)
            value = 0
            if targetPawn:
                if targetPawn.is_queen():
                    return (-math.inf, root_move)
                else:
                    value -= 1
            if sourcePawn:
                if sourcePawn.is_queen():
                    if not targetPawn:
                        value -= 0.6
            new_move = Command(moves[i][0], moves[i][1])
            new_board = board.copy_state()
            new_board.play_command(new_move)
            evaluation = minimax(new_board, your_team, enemy_team, max_depth, part, cut, root_move, score + value, depth + 1, alpha, beta, True)
            if minEval[0] != evaluation[0]:
                minEval = min(minEval, evaluation)
            if beta[0] != evaluation[0]:
                beta = min(beta, evaluation)
            if beta[0] <= alpha[0]:
                pruning = True
            i = i + 1
        answer = minEval
    return answer

def make_play(board, your_team, last_move):
    print_board(board)
    print(your_team)
    #input()
    if your_team == Team.WHITE:
        enemy_team = Team.BLACK
    else :
        enemy_team = Team.WHITE
    entities = board.get_entities()
    max_depth = 4
    cut = 4
    best_move = None
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(minimax, board, your_team, enemy_team, max_depth, i, cut) for i in range(cut)]

        for f in concurrent.futures.as_completed(results):
            move = f.result()
            if not best_move:
                best_move = move
            else:
                if best_move[0] != move[0]:
                    best_move = max(best_move, move)
            print(move)
    print('score:', best_move[0])
    selected_move = best_move[1]
    #input()
    if not best_move[1]:
        moves_available = board.get_legal_moves(your_team)
        selected_move = random.choice(moves_available)
    print('move:', selected_move)
    return selected_move
