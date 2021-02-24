from src.test.interpret import interpret_game
import unittest


class TestMovements(unittest.TestCase):

    def test_game_1(self):
        # Asserts that no exception has been raised
        interpret_game('../../resources/game_1.json')


if __name__ == '__main__':
    unittest.main()
