from enum import Enum
from src.game.game_exception import GameException
from src.game.geo import Vec2I, get_legal_positions

class Team(Enum):
    WHITE = 1
    BLACK = 2


class Event(Enum):
    MOVED_TO = 1
    MOVED_TO_CAPTURE = 2
    MOVED_TO_CREATE = 3


class Observer:

    def __init__(self):
        pass

    def update(self, obj, event, *argv):
        pass


class Observable:

    def __init__(self):
        self._observers = []

    def notify(self, event, *argv):
        for obs in self._observers:
            obs.update(self, event, *argv)

    def add_observer(self, obs):
        self._observers.append(obs)

    def remove_observer(self, obs):
        if obs in self._observers:
            self._observers.remove(obs)
        else:
            raise GameException('Given observer {} doesn\'t exists in observer list'.format(obs))


class GameObject(Observable):

    def __init__(self):
        super(GameObject, self).__init__()
        self._position = None
        self._team = None

    def get_position(self):
        return self._position

    def set_position(self, new_position):
        self._position = new_position

    def get_team(self):
        return self._team

    def set_team(self, team):
        self._team = team

    def __str__(self):
        pass


class Monkey(GameObject):

    def __init__(self, position, team):
        super(Monkey, self).__init__()
        self.set_team(team)
        self.set_position(position)

    def get_legal_moves(self, board):
        enemy_queen = board.search_queen(Team.WHITE if self._team == Team.BLACK else Team.BLACK)
        legal_positions = get_legal_positions(board, self._position)
        # Check if the new moves makes us closed from the queen
        pos_queen_distance = (enemy_queen.get_position() - self.get_position()).norm()
        final_legal_positions = []
        for new_pos in legal_positions:
            new_distance = (enemy_queen.get_position() - new_pos).norm()
            if new_distance < pos_queen_distance:
                final_legal_positions.append(new_pos)
        return final_legal_positions

    def move(self, board, new_position, capture=None):
        old_position = Vec2I(self._position.x, self._position.y)
        self.set_position(new_position)
        if capture is not None:
            self.notify(Event.MOVED_TO_CAPTURE, new_position, capture, old_position)
        else:
            self.notify(Event.MOVED_TO, new_position, old_position)

    def __str__(self):
        team = 'b' if self._team == Team.BLACK else 'w'
        return team + 'M '


class Queen(GameObject):

    def __init__(self, position, team, monkey_stack = 20):
        super(Queen, self).__init__()
        self.set_team(team)
        self.set_position(position)
        self._monkey_stack = monkey_stack

    def get_legal_moves(self, board):
        return get_legal_positions(board, self._position)

    def breed(self, board, old_position):
        if self._monkey_stack > 0:
            self._monkey_stack -= 1
            new_monkey = Monkey(old_position, self.get_team())
            board.add_entity(new_monkey)

    def move(self, board, new_position, capture=None):
        old_position = Vec2I(self._position.x, self._position.y)
        self.set_position(new_position)
        if capture is not None:
            self.notify(Event.MOVED_TO_CAPTURE, new_position, capture, old_position)
        else:
            self.notify(Event.MOVED_TO_CREATE, new_position, old_position)

    def __str__(self):
        team = 'b' if self._team == Team.BLACK else 'w'
        return team + 'Q' + str(self._monkey_stack)
