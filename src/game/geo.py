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


# def get_all_legal_pos(board, is_black_team):
#     # Builds an array with all the entities
#     cols = board.get_cols()
#     rows = board.get_rows()
#     board_list = [64 for _ in range(cols * rows)]
#     for entity in board.get_entities():
#         position = entity.get_position()
#         value = 64
#         if entity.is_queen():
#             if entity.is_black():
#                 # Black queen
#                 value = 3
#             else:
#                 # White queen
#                 value = 1
#         else:
#             if entity.is_black():
#                 # Black monkey
#                 value = 2
#             else:
#                 # White monkey
#                 value = 0
#         board_list[position.y * cols + position.x] = value
#
#     board_list = bytes(board_list)
#
#     # Computes the moves into a C function
#     moves = list_moves_c(board_list, board.get_cols(), board.get_rows(), is_black_team)
#
#     # Retrieves the result and put into a Python array
#     legal_moves = []
#     for i in range(0, len(moves), 4):
#         move_x_from = moves[i]
#         move_y_from = moves[i + 1]
#         move_x_to = moves[i + 2]
#         move_y_to = moves[i + 3]
#         if move_x_from == -1:
#             break
#         legal_moves.append((Vec2I(move_x_from, move_y_from), Vec2I(move_x_to, move_y_to)))
#
#     return legal_moves


def get_legal_positions(board, position):
    legal_positions = []
    entities = board.get_entity_map()
    this_entity = entities.get(position)
    for shift_x, shift_y in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        pos = position
        pos += Vec2I(shift_x, shift_y)
        while board.check_boundaries(pos):
            if entities.get(pos) is None:
                legal_positions.append(pos)
                pos += Vec2I(shift_x, shift_y)
            else:
                if entities.get(pos).get_team() != this_entity.get_team():
                    legal_positions.append(pos)
                break
    return legal_positions
