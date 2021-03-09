from src.test.interpret import interpret_game
from src.game.game_exception import *
from src.game.geo import Vec2I
import unittest


class TestMovements(unittest.TestCase):

    def test_game_1(self):
        # Asserts that no exception has been raised
        interpret_game('../../resources/games/game_1.json')

    def test_game_move_opponents_pieces(self):
        # Cannot move opponents pieces
        self.assertRaises(MoveOpponentPieceException, interpret_game, '../../resources/games/game_move_opponent.json')

    def test_illegal_move_direction(self):
        # Moves into a L shape
        self.assertRaises(IllegalMoveException, interpret_game, '../../resources/games/game_illegal_move_direction.json')

    def test_illegal_move_obstacle(self):
        # Cannot pass through an obstacle
        self.assertRaises(IllegalMoveException, interpret_game, '../../resources/games/game_illegal_move_obstacle.json')

    def test_illegal_move_obstacle_oblique(self):
        self.assertRaises(IllegalMoveException, interpret_game,
                          '../../resources/games/game_illegal_move_obstacle_oblique.json')

    def test_move_no_piece(self):
        self.assertRaises(NoPieceFoundException, interpret_game, '../../resources/games/game_no_piece.json')

    def test_move_further_from_queen(self):
        self.assertRaises(IllegalMoveException, interpret_game, '../../resources/games/game_move_further_from_queen.json')


class TestLegalMoves(unittest.TestCase):

    def test_get_legal_moves_queen_2x2(self):
        board = interpret_game('../../resources/games/game_get_legal_moves_queen.json')
        entities = board.get_entity_map()
        pos = Vec2I(0, 0)
        queen = entities.get(pos)
        legal_moves = queen.get_legal_moves(board)
        legal_moves_expected = [Vec2I(1, 0), Vec2I(0, 1), Vec2I(1, 1)]
        print(legal_moves)
        for move in legal_moves:
            self.assertTrue(move in legal_moves_expected)


if __name__ == '__main__':
    unittest.main()
