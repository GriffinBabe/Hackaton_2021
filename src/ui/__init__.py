import pygame
from src.game.board import Board
from src.game.entities import Observer, Team, Event, Queen
from src.game.geo import Vec2I
from src.ui.ui import UI
from src.ui.graphic_entity import draw_entity
from src.ui.graphic_entity import black_monkey_sprite, white_monkey_sprite, black_queen_sprite, white_queen_sprite
from src.game.command import Command
from src.test.game_file import read_game_file
from src.game.game_exception import GameException
import time
import threading
import sys
import queue
import re
import string


def command_thread(cmd_queue, board):
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
        cmd_queue.put(command)


if __name__ == '__main__':

    game = None
    command_queue = None
    game_from_file = False

    if len(sys.argv) == 2:
        print('Game Mode: Play game file')

        game_file = sys.argv[1]
        game_data = read_game_file(game_file)

        board_cols = game_data['cols']
        board_rows = game_data['rows']

        queen_stack = game_data['stack']
        white_queen_pos = game_data['white_queen']
        black_queen_pos = game_data['black_queen']
        command_queue = game_data['moves']

        # Default mode
        game = Board(board_cols, board_rows)
        game.add_entity(Queen(white_queen_pos, Team.WHITE, monkey_stack=queen_stack))
        game.add_entity(Queen(black_queen_pos, Team.BLACK, monkey_stack=queen_stack))

        game_from_file = True
    else:
        game = Board(8, 8)
        game.add_entity(Queen(Vec2I(3, 0), Team.WHITE, monkey_stack=8))
        game.add_entity(Queen(Vec2I(4, 7), Team.BLACK, monkey_stack=8))

    pygame.init()

    HEIGHT = 800
    WIDTH = 1000  # 800 for game 200 for info column

    fps = pygame.time.Clock()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Monkey Queen')

    window = UI(game)
    window.open_window()
    window.draw()

    if game_from_file:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYUP:
                    if len(command_queue) > 0:
                        move = command_queue.pop(0)
                        game.play_command(move)
    else:
        command_queue = queue.Queue()
        move_log = []  # All moves are registered here so they can be saved in a game file
        thread = threading.Thread(target=command_thread, args=(command_queue, game))
        thread.start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            if not command_queue.empty():
                command = command_queue.get()
                try:
                    move_log.append(command)
                    game.play_command(command)
                except GameException as e:
                    print('Wrong command: {}'.format(e))
                if game.game_over():
                    print(move_log)
                    sys.exit(0)
            time.sleep(0.05)
