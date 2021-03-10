import pygame
from src.game.board import Board
from src.game.entities import Observer, Team, Event, Queen
from src.game.geo import Vec2I
from src.ui.GraphicEntity import draw_entity
from src.ui.GraphicEntity import black_monkey_sprite, white_monkey_sprite, black_queen_sprite, white_queen_sprite
from src.game.command import Command
from src.test.game_file import read_game_file
from src.game.game_exception import GameException
import time
import threading
import sys
import queue

COLOR_BEIGE = (240, 235, 221)
COLOR_BROWN = (163, 126, 73)
COLOR_RED = (214, 119, 116)
COLOR_GREEN = (145, 214, 122)


class UI(Observer):

    def __init__(self, board, width=1000, height=800, game_file=None):
        self._width = width
        self._height = height
        self._board = board
        self._board.add_observer(self)
        self._display = None
        self._cell_size = None
        self._initialize_queen_entities()

    def _initialize_queen_entities(self):
        board_entities = self._board.get_entity_map()

    def open_window(self):
        pygame.init()
        self._display = pygame.display.set_mode((self._width, self._height))
        cell_width = (self._width - 200) / self._board.get_cols()
        cell_height = self._height / self._board.get_rows()
        self._cell_size = int(min(cell_width, cell_height))
        pygame.display.set_caption('Monkey Queen')
        pygame.display.set_icon(white_monkey_sprite)

    def update(self, obj, event, *argv):
        if event == Event.MOVED_TO:
            new_position = argv[0]
            old_position = argv[1]
            self.draw(old_position, new_position)
        elif event == Event.MOVED_TO_CAPTURE:
            new_position = argv[0]
            captured_piece = argv[1]
            old_position = argv[2]
            self.draw(old_position, new_position)
        elif event == Event.MOVED_TO_CREATE:
            new_position = argv[0]
            old_position = argv[1]
            self.draw(old_position, new_position)

    def draw(self, old_position=None, new_position=None):
        font = pygame.font.Font(pygame.font.get_default_font(), 25)
        surface = pygame.Surface((self._board.get_cols() * self._cell_size, self._board.get_rows() * self._cell_size))
        for x in range(self._board.get_cols()):
            for y in range(self._board.get_rows()):
                if (x + y) % 2 == 0:
                    color = COLOR_BEIGE
                else:
                    color = COLOR_BROWN
                pygame.draw.rect(surface, color, pygame.rect.Rect(x * self._cell_size, y * self._cell_size, self._cell_size, self._cell_size))

        if old_position is not None:
            pygame.draw.rect(surface, COLOR_RED, pygame.rect.Rect(old_position.x * self._cell_size, old_position.y * self._cell_size, self._cell_size, self._cell_size))
        for entity in self._board.get_entity_map().values():
            draw_entity(entity, surface, self._cell_size)

        for x in range(self._board.get_cols()):
            text_surface = font.render(str(x + 1), True, COLOR_GREEN)
            surface.blit(text_surface, (x * self._cell_size + 5, 5))
        for y in range(self._board.get_rows()):
            text_surface = font.render(str(y + 1), True, COLOR_GREEN)
            surface.blit(text_surface, (5, y * self._cell_size + 5))

        self._display.blit(surface, (0, 0))
        pygame.display.flip()


def command_thread(cmd_queue, board):
    while True:
        time.sleep(0.05)
        if board.game_over():
            break  # Thread closes once the game is over

        move_from_str = input('Move from: ')
        move_to_str = input('Move to: ')

        move_from_ls = move_from_str.split(', ')
        move_to_ls = move_to_str.split(', ')

        move_from = Vec2I(int(move_from_ls[0]) - 1, int(move_from_ls[1]) - 1)
        move_to = Vec2I(int(move_to_ls[0]) - 1, int(move_to_ls[1]) - 1)
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
