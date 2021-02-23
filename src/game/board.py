from src.game.entities import GameObject, Team, Event
from src.game.geo import Vec2I


class Board:

    def __init__(self, cols=12, rows=12):
        self._cols = cols
        self._rows = rows
        self._entities = []
        self._turn_count = 1
        self._team_turn = Team.WHITE

    def add_entity(self, obj):
        # Checks that entity is in the bounds of the board
        self._entities.append(obj)
        obj.add_observer(self)  # The board is an observer to the pieces

    def get_cols(self):
        return self._cols

    def get_rows(self):
        return self._rows

    def draw(self):
        """
        Draws the board representation in the console
        :return:
        """
        out_str = 3 * ' '
        for x in range(self._cols):
            out_str += str(x + 1) + 3 * ' '
        out_str += '\n'
        for y in range(self._rows):
            out_str += str(y + 1) + ' '
            for x in range(self._cols):
                object = self._get_gameobject_from_pos(Vec2I(x, y))
                if object is not None:
                    out_str += str(object)
                else:
                    out_str += 3 * ' '
                if x != self._cols - 1:
                    out_str += '|'
            if y != self._rows - 1:
                out_str += '\n' + '  ' + ('-' * 4 * self._cols) + '\n'
        if self._team_turn == Team.BLACK:
            out_str += '\nBlack to play.\n'
        else:
            out_str += '\nWhite to play.\n'
        print(out_str)

    def _get_gameobject_from_pos(self, pos):
        for obj in self._entities:
            obj_pos = obj.get_position()
            if obj_pos == pos:
                return obj
        return None

    def _check_boundaries(self, pos):
        if pos.x < 0 or pos.y < 0:
            return False
        if pos.x >= self._cols or pos.y >= self._rows:
            return False
        return True

    def play_command(self, command):
        pos_from = command.get_from()
        pos_to = command.get_to()

        if not self._check_boundaries(pos_from) or not self._check_boundaries(pos_to):
            raise Exception('Out of bounds position was given.')

        piece_from = self._get_gameobject_from_pos(pos_from)

        # Cannot move opponent's pieces
        if piece_from.get_team() != self._team_turn:
            raise Exception('Cannot move opponent\'s pieces.')

        if piece_from is None:
            raise Exception('No piece was found in this position.')

        if self._team_turn == Team.WHITE:
            self._team_turn = Team.BLACK
        else:
            self._team_turn = Team.WHITE
            self._turn_count += 1

        piece_from.move(self, pos_to)

    def update(self, obj, event, *argv):
        if event == Event.MOVED_TO:
            self.draw()
        elif event == Event.MOVED_TO_CAPTURE:
            self.draw()
        elif event == Event.MOVED_TO_CREATE:
            self.draw()
