from src.game.entities import Team
from src.game.geo import Vec2I
import random


def make_play(board, your_team, last_move):
    plays = board.get_legal_moves(your_team)
    random_play = random.choice(plays)
    return random_play
