class GameException(Exception):
    pass


class MoveOpponentPieceException(GameException):
    pass


class NoPieceFoundException(GameException):
    pass


class IllegalMoveException(GameException):
    pass


class OutOfBoundsException(GameException):
    pass
