import math


class Vec2I:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return Vec2I(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash(str(self.x) + '-' + str(self.y))

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def parse_from_list(split_list):
        return Vec2I(int(split_list[0]) - 1, int(split_list[1]) - 1)


Vec2I.parse_from_list = staticmethod(Vec2I.parse_from_list)


def check_collision(board, old_pos, new_pos):
    entities = board.get_entity_map()
    # Checks if there is no collision in the path
    delta_pos = (new_pos - old_pos)

    # Create an array of the cells between the destination position and the old position
    position = None
    if delta_pos.y == 0:  # Horizontal
        position = [Vec2I(old_pos.x + dx, old_pos.y) for dx in range(1, delta_pos.x - 1)]
    elif delta_pos.x == 0:  # Vertical
        position = [Vec2I(old_pos.x, old_pos.y + dy) for dy in range(1, delta_pos.y - 1)]
    elif abs(delta_pos.y == delta_pos.x):  # Oblique
        position = [Vec2I(old_pos.x + dx, old_pos + dy) for dx, dy in zip(range(1, delta_pos.x - 1), range(1, delta_pos.y - 1))]

    is_obstacle = False
    where_obstacle = None

    for pos in position:
        if entities.get(pos) is not None:
            is_obstacle = True
            where_obstacle = pos
            break

    if is_obstacle:
        return False, entities.get(where_obstacle)

    captured_piece = entities.get(new_pos)

    return True, captured_piece
