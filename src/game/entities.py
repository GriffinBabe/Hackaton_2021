from enum import Enum


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

    def update(self, event, *argv):
        pass


class Observable:

    def __init__(self):
        self._observers = []

    def notify(self, event, *argv):
        for obs in self._observers:
            obs.update(event, *argv)

    def add_observer(self, obs):
        self._observers.append(obs)

    def remove_observer(self, obs):
        if obs in self._observers:
            self._observers.remove(obs)
        else:
            raise Exception('Given observer {} doesn\'t exists in observer list'.format(obs))


class GameObject(Observable):

    def __init__(self):
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
        self.set_team(team)
        self.set_position(position)

    def move(self, board, new_position):
        # TODO: Check and act
        self.notify(Event.MOVED_TO, new_position)

    def __str__(self):
        team = 'b' if self._team == Team.BLACK else 'w'
        return team + 'M'


class Queen(GameObject):

    def __init__(self, position, team, monkey_stack = 20):
        self.set_team(team)
        self.set_position(position)
        self._monkey_stack = monkey_stack

    def move(self, board, new_position):
        # TODO: Checkand act
        self.notify(Event.MOVED_TO, new_position)

    def __str__(self):
        team = 'b' if self._team == Team.BLACK else 'w'
        return team + 'Q' + str(self._monkey_stack)
