import random


def make_play(board, your_team, last_move):
    """
    Example of a very stupid AI. Don't do this at home.
    """
    all_moves = board.get_legal_moves(your_team)
    selected_move = random.choice(all_moves)
    return selected_move
