from src.game.board import Board
from src.game.entities import Team, Queen
from src.game.geo import Vec2I
from src.ai.interface import MonkeyQueenGameInterface
from src.ai.monte_carlo import MonteCarloTree, next_coup
from src.ui.ui import UI
from src.game.command import Command
import pygame
import time
import string


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

    white_queen = Queen(Vec2I(3, 0), Team.WHITE, monkey_stack=12)
    black_queen = Queen(Vec2I(4, 7), Team.BLACK, monkey_stack=12)

    board.add_entity(white_queen)
    board.add_entity(black_queen)

    graphics = UI(board)
    graphics.open_window()

    game_interface = MonkeyQueenGameInterface(board)

    AI = [Team.WHITE, Team.BLACK]

    while board.get_winner() is None:
        current_player = board.get_turn()
        _ = pygame.event.get()

        if current_player in AI:
            mcts = MonteCarloTree(current_player, game_interface, None)
            iterations = 5000
            for _ in range(iterations):
                mcts.tree_search()
            best_coup = next_coup(mcts)
            game_interface.make_play(best_coup)
        else:
            command = get_command(board)
            board.play_command(command)
