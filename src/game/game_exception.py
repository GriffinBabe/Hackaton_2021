class GameException(Exception):
    pass


class MoveOpponentPieceException(GameException):
    pass


class NoPieceFound(GameException):
    pass


class IllegalMove(GameException):
    pass


class OutOfBounds(GameException):
    pass
