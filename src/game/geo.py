import math


class Vec2I:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vec2I(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2I(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash(str(self.x) + '-' + str(self.y))

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def parse_from_list(split_list):
        return Vec2I(int(split_list[0]) - 1, int(split_list[1]) - 1)


Vec2I.parse_from_list = staticmethod(Vec2I.parse_from_list)


def get_legal_positions(board, position):
    legal_positions = []
    entities = board.get_entity_map()
    # Horizontal left moves
    for x in range(position.x + 1, board.get_cols()):
        pos = Vec2I(x, position.y)
        if entities.get(pos) is None:
            legal_positions.append(pos)
        else:
            legal_positions.append(pos)
            break
    # Horizontal right moves
    for x in range(position.x - 1, -1, -1):
        pos = Vec2I(x, position.y)
        if entities.get(pos) is None:
            legal_positions.append(pos)
        else:
            legal_positions.append(pos)
            break
    # Vertical down moves
    for y in range(position.y + 1, board.get_rows()):
        pos = Vec2I(position.x, y)
        if entities.get(pos) is None:
            legal_positions.append(pos)
        else:
            legal_positions.append(pos)
            break
    # Vertical up moves
    for y in range(position.y -1, -1, -1):
        pos = Vec2I(position.x, y)
        if entities.get(pos) is None:
            legal_positions.append(pos)
        else:
            legal_positions.append(pos)
            break
    # Oblique moves
    for shift_x, shift_y in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        pos = position
        pos += Vec2I(shift_x, shift_y)
        while board.check_boundaries(pos):
            if entities.get(pos) is None:
                legal_positions.append(pos)
                pos += Vec2I(shift_x, shift_y)
            else:
                legal_positions.append(pos)
                break
    return legal_positions
