"""===========================================================================
hackaton best 2021: IA Challenge
L°Nakira@Hwtechs
============================================================================"""
from src.game.entities import Team, Monkey, Queen
from src.game.board import Board
from src.game.geo import Vec2I
from src.game.command import Command
import random
import math

# Define your persistent variables here


def make_play(board, your_team, last_move):
    current_board1 = board.copy_state()
    enemy_team = Team.WHITE if your_team == Team.BLACK else Team.BLACK
    print(enemy_team)
    enemy_queen = board.search_queen(enemy_team)

    noeud1 = 0
    score1 = []
    all_moves = board.get_legal_moves(your_team)
    for move in all_moves:
        board = current_board1.copy_state()
        enemy_queen = board.search_queen(enemy_team)
        if move[1] == enemy_queen.get_position():
                    print("sortie1")
                    return move
        move_command = Command(move[0] , move[1])
        board.play_command(move_command)

        current_board2 = board.copy_state()
        noeud2 = 0
        score2=[]
        opponent_possible_responses = board.get_legal_moves()
        try :
            for  opponent_possible_move in opponent_possible_responses :
                board = current_board2.copy_state()
                opponent_possible_move_command = Command(opponent_possible_move[0], opponent_possible_move[1])
                board.play_command(opponent_possible_move_command)
                if  opponent_possible_move[1] == enemy_queen.get_position() :
                    print("ko")
                    break
                current_board3 = board.copy_state()
                noeud3 = 0
                enemy_queen = board.search_queen(enemy_team)
                responses = board.get_legal_moves()
                for  response_move in responses :
                    board = current_board3
                    enemy_queen = board.search_queen(enemy_team)
                    try:
                        response_move_command = Command(response_move[0], response_move[1])
                        board.play_command(response_move_command)
                        if board.game_over :
                            return move
                        score3 = 100 - 10*getdistance(response_move[1],enemy_queen)
                        noeud3 = score3 if score3 >= noeud3 else noeud3
                    except Exception:
                        pass
                score2.append(noeud3)
            noeud2 = min(score2)
        except Exception:
            pass
        
        score1.append(noeud2)

    if len(score1) == len(all_moves) :
        noeud1 = max(score1)
        selected_move = all_moves[score1.index(noeud1)]
        return selected_move
    else:
        print (" y a un pépin kekpart :( ")

def getdistance(yourpiece,enemypiece):
    enemy_piece_position = enemypiece.get_position()
    distance = math.sqrt( (enemy_piece_position.x - yourpiece.x)**2 + (enemy_piece_position.y - yourpiece.y)**2 )
    return distance