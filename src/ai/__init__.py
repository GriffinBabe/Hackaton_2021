from src.game.board import Board
from src.game.entities import Team, Queen
from src.game.geo import Vec2I
from src.game.game_exception import GameException
from src.ui.ui import UI
from src.ai.my_ai_random import make_play
from src.game.command import Command
from src.ai.interface import MonkeyQueenGameInterface
from src.ai.monte_carlo import MonteCarloTree
import pygame
import time
import string

ncoup = 1


def next_coup(root):
    global ncoup
    """
    :return: next coup with highest value
    """
    max_ = root.children[0]
    for elem in root.children:
        print(elem.val / elem.visits)
        if (elem.val / elem.visits) > (max_.val / max_.visits):
            max_ = elem
    ncoup *= len(root.children)
    print("max", (max_.val / max_.visits))
    return max_.coup_played


# noinspection DuplicatedCode
def get_command(board):
    while True:
        time.sleep(0.05)
        if board.game_over():
            break  # Thread closes once the game is over

        team_to_play = board.get_turn()

        print('{} to play...'.format('White' if team_to_play == Team.WHITE else 'Black'))
        move_from_str = input('Move from: ')
        move_to_str = input('Move to: ')

        letters = string.ascii_lowercase

        move_from_ls = list(move_from_str)
        move_to_ls = list(move_to_str)

        try:
            move_from_ls[0] = letters.index(move_from_ls[0].lower())
            move_to_ls[0] = letters.index(move_to_ls[0].lower())
            move_from = Vec2I(int(move_from_ls[0]), int(move_from_ls[1]))
            move_to = Vec2I(int(move_to_ls[0]), int(move_to_ls[1]))
        except ValueError:
            print('Please specify a letter then a number with no space between them. Example: d0 and d3')
            continue

        command = Command(move_from, move_to)
        return command


if __name__ == '__main__':
    board = Board(cols=8, rows=8)

    game_interface = MonkeyQueenGameInterface(board)

    white_queen = Queen(Vec2I(3, 0), Team.WHITE, monkey_stack=12)
    black_queen = Queen(Vec2I(4, 7), Team.BLACK, monkey_stack=12)

    board.add_entity(white_queen)
    board.add_entity(black_queen)

    graphics = UI(board)
    graphics.open_window()

    AI = [Team.WHITE, Team.BLACK]

    last_move = None

    while board.get_winner() is None:
        current_player = board.get_turn()

        # Check if there are still legal moves
        legal_moves = board.get_legal_moves(current_player)
        if len(legal_moves) == 0:
            print('No legal moves exists for team {}. Team {} wins.'
                  .format('white' if current_player == Team.WHITE else 'black', 'black' if current_player == Team.BLACK else 'white'))

        _ = pygame.event.get()

        if current_player in AI:
            MC = MonteCarloTree(current_player, game_interface, None)
            iterations = 1000
            c = 0
            while iterations > 0:
                print(iterations)
                if iterations % 2000 == 0:
                    print("processing machine coup ... %i/10" % c)
                    c += 1
                MC.tree_search()
                iterations -= 1
            best_coup = next_coup(MC)
            game_interface.make_play(best_coup)
            # board_copy = board.copy_state()
            # play = make_play(board_copy, current_player, last_move)
            # board.play_command(Command(play[0], play[1]))
            # last_move = (play[0], play[1])
        else:
            while True:
                try:
                    command = get_command(board)
                    board.play_command(command)
                    last_move = \
                        (Vec2I(command.get_from().x, command.get_from().y), command.get_to().x, command.get_to().y)
                    break
                except GameException as e:
                    print('Wrong move: {}'.format(e))

    time.sleep(3)
    if board.get_winner() is not None:
        print(board.get_winner())
