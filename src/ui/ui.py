import pygame
from src.game.entities import Observer, Team, Event, Queen
from src.ui.graphic_entity import draw_entity
from src.ui.graphic_entity import black_monkey_sprite, white_monkey_sprite, black_queen_sprite, white_queen_sprite

COLOR_BEIGE = (240, 235, 221)
COLOR_BROWN = (163, 126, 73)
COLOR_RED = (214, 119, 116)
COLOR_GREEN = (145, 214, 122)


class UI(Observer):

    def __init__(self, board, width=1000, height=800, game_file=None):
        super().__init__()
        self._width = width
        self._height = height
        self._board = board
        self._board.add_observer(self)
        self._display = None
        self._cell_size = None
        self._initialize_queen_entities()

    def _initialize_queen_entities(self):
        board_entities = self._board.get_entity_map()

    def open_window(self):
        pygame.init()
        self._display = pygame.display.set_mode((self._width, self._height))
        cell_width = (self._width - 200) / self._board.get_cols()
        cell_height = self._height / self._board.get_rows()
        self._cell_size = int(min(cell_width, cell_height))
        pygame.display.set_caption('Monkey Queen')
        pygame.display.set_icon(white_monkey_sprite)

    def update(self, obj, event, *argv):
        if event == Event.MOVED_TO:
            new_position = argv[0]
            old_position = argv[1]
            self.draw(old_position, new_position)
        elif event == Event.MOVED_TO_CAPTURE:
            new_position = argv[0]
            captured_piece = argv[1]
            old_position = argv[2]
            self.draw(old_position, new_position)
        elif event == Event.MOVED_TO_CREATE:
            new_position = argv[0]
            old_position = argv[1]
            self.draw(old_position, new_position)

    def draw(self, old_position=None, new_position=None):
        font = pygame.font.Font(pygame.font.get_default_font(), 25)
        surface = pygame.Surface((self._board.get_cols() * self._cell_size, self._board.get_rows() * self._cell_size))
        for x in range(self._board.get_cols()):
            for y in range(self._board.get_rows()):
                if (x + y) % 2 == 0:
                    color = COLOR_BEIGE
                else:
                    color = COLOR_BROWN
                pygame.draw.rect(surface, color, pygame.rect.Rect(x * self._cell_size, y * self._cell_size, self._cell_size, self._cell_size))

        if old_position is not None:
            pygame.draw.rect(surface, COLOR_RED, pygame.rect.Rect(old_position.x * self._cell_size, old_position.y * self._cell_size, self._cell_size, self._cell_size))
        for entity in self._board.get_entity_map().values():
            draw_entity(entity, surface, self._cell_size)

        for x in range(self._board.get_cols()):
            text_surface = font.render(str(x + 1), True, COLOR_GREEN)
            surface.blit(text_surface, (x * self._cell_size + 5, 5))
        for y in range(self._board.get_rows()):
            text_surface = font.render(str(y + 1), True, COLOR_GREEN)
            surface.blit(text_surface, (5, y * self._cell_size + 5))

        self._display.blit(surface, (0, 0))
        pygame.display.flip()
