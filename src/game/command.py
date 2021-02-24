class Command:

    def __init__(self, pos_from, pos_to):
        self._pos_from = pos_from
        self._pos_to = pos_to

    def get_from(self):
        return self._pos_from

    def get_to(self):
        return self._pos_to

    def __str__(self):
        return '{}, {} -> {}, {}'.format(self._pos_from.x, self._pos_from.y, self._pos_to.x, self._pos_to.y)
