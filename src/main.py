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
    from_x = int(str_from[0]) - 1
    from_y = int(str_from[1]) - 1

    pos_from = Vec2I(from_x, from_y)

    str_to = input('Piece to (x, y): ')
    str_to = str_to.split(',')
    to_x = int(str_to[0]) - 1
    to_y = int(str_to[1]) - 1

    pos_to = Vec2I(to_x, to_y)

    command = Command(pos_from, pos_to)

    try:
        board.play_command(command)
    except Exception as exc:
        print(exc)
