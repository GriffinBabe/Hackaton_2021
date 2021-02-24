from enum import Enum
from src.game.geo import check_collision

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
            raise Exception('Given observer {} doesn\'t exists in observer list'.format(obs))


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

    def is_legal(self, board, new_position):
        # Checks if a move is legal (if the direction is horizontal, vertical or oblique)
        delta_pos = self.get_position() - new_position
        good_direction = False

        # Move in the same position => Illegal
        if delta_pos.x == 0 and delta_pos.y == 0:
            return False

        # Move horizontally or vertically
        if delta_pos.x == 0 or delta_pos.y == 0:
            good_direction = True

        # Move in oblique
        if abs(delta_pos.x) == abs(delta_pos.y):
            good_direction = True

        if not good_direction:
            return False

        # Enemy queen reference
        team_color = self.get_team()
        enemy_queen = board.search_queen(Team.BLACK if team_color == Team.WHITE else Team.WHITE)

        # Checks if the new position makes the monkey closer to the enemy queen
        old_distance = (enemy_queen - self.get_position()).norm()
        new_distance = (enemy_queen - new_position).norm()

        if old_distance < new_distance:
            return False

        # Checks collision with other units
        return check_collision(board, self.get_position(), new_position)

    def move(self, board, new_position, capture=None):
        # TODO: Check and act
        self.set_position(new_position)
        if capture is not None:
            self.notify(Event.MOVED_TO_CAPTURE, new_position, capture)
        else:
            self.notify(Event.MOVED_TO, new_position)

    def __str__(self):
        team = 'b' if self._team == Team.BLACK else 'w'
        return team + 'M'


class Queen(GameObject):

    def __init__(self, position, team, monkey_stack = 20):
        super(Queen, self).__init__()
        self.set_team(team)
        self.set_position(position)
        self._monkey_stack = monkey_stack

    def is_legal(self, board, new_position):
        # Checks if a move is legal (if the direction is horizontal, vertical or oblique)
        delta_pos = self.get_position() - new_position
        good_direction = False

        # Move in the same position => Illegal
        if delta_pos.x == 0 and delta_pos.y == 0:
            return False

        # Move horizontally or vertically
        if delta_pos.x == 0 or delta_pos.y == 0:
            good_direction = True

        # Move in oblique
        if abs(delta_pos.x) == abs(delta_pos.y):
            good_direction = True

        if not good_direction:
            return False

        # Checks collision with other units
        return check_collision(board, self.get_position(), new_position)

    def breed(self, board, old_position):
        if self._monkey_stack > 0:
            self._monkey_stack -= 1
            new_monkey = Monkey(old_position, self.get_team())
            board.add_entity(new_monkey)

    def move(self, board, new_position, capture=None):
        old_position = self.get_position()
        self.set_position(new_position)
        if capture is not None:
            self.notify(Event.MOVED_TO_CAPTURE, new_position, capture)
        else:
            self.notify(Event.MOVED_TO_CREATE, new_position, old_position)

    def __str__(self):
        team = 'b' if self._team == Team.BLACK else 'w'
        return team + 'Q' + str(self._monkey_stack)
