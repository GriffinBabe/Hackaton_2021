from src.game.board import Board
from src.game.entities import Monkey, Queen, Team
from src.game.geo import Vec2I

ROWS = 8
COLS = 8

white_queen = Queen(Vec2I(3, 0), Team.WHITE, monkey_stack=8)
black_queen = Queen(Vec2I(4, 7), Team.BLACK, monkey_stack=8)

board = Board(cols=COLS, rows=ROWS)
board.add_entity(white_queen)
board.add_entity(black_queen)

board.draw()
