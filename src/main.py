from src.game.board import Board
from src.game.entities import Monkey, Queen, Team
from src.game.command import Command
from src.game.geo import Vec2I

ROWS = 8
COLS = 8

white_queen = Queen(Vec2I(3, 0), Team.WHITE, monkey_stack=8)
black_queen = Queen(Vec2I(4, 7), Team.BLACK, monkey_stack=8)

board = Board(cols=COLS, rows=ROWS)
board.add_entity(white_queen)
board.add_entity(black_queen)

board.draw()

while True:
    str_from = input('Piece from (x, y): ')
    str_from = str_from.split(',')
    pos_from = Vec2I.parse_from_list(str_from)

    str_to = input('Piece to (x, y): ')
    str_to = str_to.split(', ')
    pos_to = Vec2I.parse_from_list(str_to)

    command = Command(pos_from, pos_to)

    try:
        board.play_command(command)
    except Exception as exc:
        print(exc)
