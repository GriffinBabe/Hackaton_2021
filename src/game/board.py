from src.game.entities import GameObject, Team, Event, Queen, Observable, Observer
from src.game.game_exception import *
from src.game.geo import Vec2I
from copy import deepcopy

class Board(Observable, Observer):

    def __init__(self, cols=12, rows=12, console=False):
        Observable.__init__(self)
        self._cols = cols
        self._rows = rows
        self._entities = []
        self._turn_count = 1
        self._team_turn = Team.WHITE
        self._observers = []
        self._game_over = False
        self._winner = None
        self._console = False

    def game_over(self):
        return self._game_over

    def get_winner(self):
        return self._winner

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

    def get_entity_map(self):
        map = {}
        for obj in self._entities:
            map[obj.get_position()] = obj
        return map

    def get_entities(self):
        return self._entities

    def get_legal_moves(self, team=None):
        if team is None:
            team = self._team_turn
        legal_moves = []
        for entity in self._entities:
            if entity.get_team() == team:
                positions = entity.get_legal_moves(self)
                for pos in positions:
                    if pos != entity.get_position():
                        legal_moves.append((entity.get_position(), pos))
        return legal_moves

    # def get_all_legal_moves(self, team=None):
    #     if team is None:
    #         team = self._team_turn
    #     return get_all_legal_pos(self, team == Team.BLACK)

    def _get_gameobject_from_pos(self, pos):
        for obj in self._entities:
            obj_pos = obj.get_position()
            if obj_pos == pos:
                return obj
        return None

    def check_boundaries(self, pos):
        if pos.x < 0 or pos.y < 0:
            return False
        if pos.x >= self._cols or pos.y >= self._rows:
            return False
        return True

    def search_queen(self, team):
        for obj in self._entities:
            if isinstance(obj, Queen):
                if obj.get_team() == team:
                    return obj
        return None

    def play_command(self, command):
        pos_from = command.get_from()
        pos_to = command.get_to()

        if not self.check_boundaries(pos_from) or not self.check_boundaries(pos_to):
            raise OutOfBoundsException('Out of bounds position was given.')

        piece_from = self._get_gameobject_from_pos(pos_from)

        if piece_from is None:
            raise NoPieceFoundException('No piece was found in this position.')

        # Cannot move opponent's pieces
        if piece_from.get_team() != self._team_turn:
            raise MoveOpponentPieceException('Cannot move opponent\'s pieces.')

        legal_moves = piece_from.get_legal_moves(self)
        capture = self._get_gameobject_from_pos(pos_to)

        if pos_to not in legal_moves:
            raise IllegalMoveException('Illegal move')

        if self._team_turn == Team.WHITE:
            self._team_turn = Team.BLACK
        else:
            self._team_turn = Team.WHITE
            self._turn_count += 1

        piece_from.move(self, pos_to, capture=capture)

    def update(self, obj, event, *argv):
        if event == Event.MOVED_TO:
            pass
        elif event == Event.MOVED_TO_CAPTURE:
            captured_piece = argv[1]
            if isinstance(captured_piece, Queen):
                if captured_piece.get_team() == Team.WHITE:
                    self._winner = Team.BLACK
                elif captured_piece.get_team() == Team.BLACK:
                    self._winner = Team.WHITE
                self._game_over = True
            else:
                self._entities.remove(captured_piece)
        elif event == Event.MOVED_TO_CREATE:
            old_position = argv[1]
            obj.breed(self, old_position)
        if self._console:
            self.draw()
        self.notify(event, *argv)

    def copy_state(self):
        temp_observers = self._observers
        self._observers = []

        new_state = deepcopy(self)
        new_state._observers.clear()

        self._observers = temp_observers

        return new_state

    def get_turn(self):
        return self._team_turn
