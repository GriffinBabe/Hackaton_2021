import pygame
from src.game.entities import Team, Monkey, Queen


black_monkey_sprite = pygame.image.load('resources/sprites/black_monkey.png')
white_monkey_sprite = pygame.image.load('resources/sprites/white_monkey.png')
black_queen_sprite = pygame.image.load('resources/sprites/black_queen.png')
white_queen_sprite = pygame.image.load('resources/sprites/white_queen.png')


def draw_entity(entity, surface, cell_size):

    # Code de branleur
    if type(entity) is Queen:
        if entity.get_team() == Team.WHITE:
            sprite = white_queen_sprite
        else:
            sprite = black_queen_sprite
    elif type(entity) is Monkey:
        if entity.get_team() == Team.WHITE:
            sprite = white_monkey_sprite
        else:
            sprite = black_monkey_sprite

    position = entity.get_position()
    this_sprite = pygame.transform.scale(sprite, (cell_size, cell_size))
    surface.blit(this_sprite, (position.x * cell_size, position.y * cell_size))
