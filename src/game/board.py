from src.game.entities import GameObject
from src.game.geo import Vec2I


class Board:

    def __init__(self, cols=12, rows=12):
        self._cols = cols
        self._rows = rows
        self._entities = []

    def add_entity(self, obj):
        self._entities.append(obj)

    def get_cols(self):
        return self._cols

    def get_rows(self):
        return self._rows

    def draw(self):
        """
        Draws the board representation in the console
        :return:
        """
        out_str = ''
        for y in range(self._rows):
            for x in range(self._cols):
                object = self._get_gameobject_from_pos(Vec2I(x, y))
                if object is not None:
                    out_str += str(object)
                else:
                    out_str += 3 * ' '
                if x != self._cols - 1:
                    out_str += '|'
            if y != self._rows - 1:
                out_str += '\n' + ('-' * 4 * self._cols) + '\n'
        print(out_str)

    def _get_gameobject_from_pos(self, pos):
        for obj in self._entities:
            obj_pos = obj.get_position()
            if obj_pos == pos:
                return obj
        return None
