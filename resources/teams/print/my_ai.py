from src.game.entities import Team, Monkey, Queen
from src.game.board import Board
from src.game.geo import Vec2I
from src.game.command import Command
import random

"""
Code your AI in this file.
"""

# Define your persistent variables here


def make_play(board, your_team, last_move):
    """
    Example of a very stupid AI. Don't do this at home.
    ...
    ...
    Keep it simple...
    """

    entities = board.get_entities()

    # Team choice
    enemy_team = None
    if your_team == Team.WHITE:
        enemy_team = Team.BLACK
    else:
        enemy_team = Team.WHITE
    entity_map = board.get_entity_map()

    # Possible moves
    all_possible_moves = board.get_legal_moves(your_team)
    all_possible_enemy_moves = board.get_legal_moves(enemy_team)
    potential_moves = [all_possible_moves[i][1] for i in range(len(all_possible_moves))]
    potential_enemy_moves = [all_possible_enemy_moves[i][1] for i in range(len(all_possible_enemy_moves))]


    # Queens
    your_queen = board.search_queen(your_team)
    your_queen_position = your_queen.get_position()  # YOUR QUEEN POS
    enemy_queen = board.search_queen(enemy_team)
    enemy_queen_position = enemy_queen.get_position()  # ENEMY QUEEN POS

    potential_queen_moves = your_queen.get_legal_moves(board)  # YOUR QUEEN MOVES
    potential_enemy_queen_moves = enemy_queen.get_legal_moves(board)  # ENEMY QUEEN MOVES

    # Sorting the potential moves
    if last_move[0] in potential_moves:
        potential_moves.remove(last_move[0])
    for posi in potential_moves:
        if posi in potential_enemy_moves:
            potential_moves.remove(posi)
        for x in range(int(last_move[0].x) - 1, int(last_move[0].x) + 2):
            for y in range(int(last_move[0].y) - 1, int(last_move[0].y) + 2):
                if Vec2I(x, y) in potential_moves:
                    potential_moves.remove(Vec2I(x, y))

    # Monkeys
    your_monkey_position = []  # YOUR MONKEYS POS
    enemy_monkey_position = []  # ENEMY MONKEYS POS
    for entity in entities:
        team = entity.get_team()
        position = entity.get_position()
        if type(entity) == Monkey and team == your_team:
            your_monkey_position.append(position)
        elif type(entity) == Monkey and team != your_team:
            enemy_monkey_position.append(position)

    number_of_monkeys = 12 - your_queen.get_stack()  # NUMBER OF MONKEYS
    number_of_enemy_monkeys = 12 - enemy_queen.get_stack()  # NUMBER OF ENEMY MONKEYS

    potential_monkey_moves1 = set(potential_moves) - set(potential_queen_moves)
    potential_monkey_moves2 = set(potential_moves) & set(potential_queen_moves)
    potential_monkey_moves = []  # YOUR MONKEYS MOVES
    for element in potential_monkey_moves1:
        potential_monkey_moves.append(element)
    for element in potential_monkey_moves2:
        potential_monkey_moves.append(element)
    potential_enemy_monkey_moves1 = set(potential_enemy_moves) - set(potential_enemy_queen_moves)
    potential_enemy_monkey_moves2 = set(potential_enemy_moves) & set(potential_enemy_queen_moves)
    potential_enemy_monkey_moves = []  # ENEMY MONKEYS MOVES
    for element in potential_enemy_monkey_moves1:
        potential_enemy_monkey_moves.append(element)
    for element in potential_enemy_monkey_moves2:
        potential_enemy_monkey_moves.append(element)

    L_around_enemy_queen = []  # L AROUND QUEEN
    for x in range(enemy_queen_position.x - 2, enemy_queen_position.x + 3):
        for y in range(enemy_queen_position.y - 2, enemy_queen_position.y + 3):
            if Vec2I(x, y) not in potential_enemy_queen_moves and Vec2I(x, y) is not your_queen_position:
                L_around_enemy_queen.append(Vec2I(x, y))

    new_position = Vec2I(None, None)

    mouv = 0
    while mouv < (len(potential_enemy_moves) - 1) and potential_enemy_moves[mouv] not in entity_map:
        mouv += 1
    dict = dico_moves(all_possible_moves)
    # STEP 1
    # Can we take the enemy queen ?
    if potential_enemy_moves[mouv] in entity_map and potential_enemy_moves[mouv] in dict and \
            ispossible(dict[potential_enemy_moves[mouv]], potential_moves):
        old_position = potential_enemy_moves[mouv]
        new_position = dict[potential_enemy_moves[mouv]]
        # STEP 2
    # Avoid dangerous position
    #and str(potential_enemy_moves[mouv]) in str(your_monkey_position)
    elif potential_enemy_moves[mouv] not in entity_map or \
            potential_enemy_moves[mouv] not in entity_map and str(potential_enemy_moves[mouv]) == str(your_queen_position):
        old_position = your_queen_position

        for element in potential_enemy_moves:

            # Avoid to move our queen to a dangerous tile
            if element in potential_queen_moves:
                potential_queen_moves.remove(element)
                new_position = random.choice(potential_queen_moves)

            # If the queen is in danger, we have to move it
            if element is your_queen_position:

                # Move the Queen
                if potential_queen_moves != []:
                    old_position = your_queen_position
                    new_position = random.choice(potential_queen_moves)

                # Block the danger with a Monkey
                else:
                    # Tiles selection
                    for x in range(your_queen_position.x - 1, your_queen_position.x + 2):
                        for y in range(your_queen_position.y - 1, your_queen_position.y + 2):

                            # Can we move a monkey there ?

                            best_position = Vec2I(None, None)
                            for ent in your_monkey_position:
                                possibilities = ent[0].get_legal_moves(board)
                                old_position = ent[1]
                                new_position = random.choice(possibilities)
                                if Vec2I(x, y) in possibilities and ispossible(Vec2I(x, y), potential_moves):
                                    old_position = ent[1]
                                    best_position = Vec2I(x, y)
                            if best_position != Vec2I(None, None):
                                new_position = best_position

    # Monkey vs Monkey
    else:
        moov = 0
        while moov < (len(potential_monkey_moves) - 1) and potential_monkey_moves[moov] not in enemy_monkey_position:
            moov += 1
        # Monkey attacks monkey
        if potential_monkey_moves[moov] in enemy_monkey_position and \
                ispossible(potential_monkey_moves[moov], potential_moves):
            dico = dico_moves(all_possible_moves)
            old_position = dico[potential_monkey_moves[moov]]
            new_position = potential_monkey_moves[moov]
        else:
            # If no monkey can attack any monkey
            dico = dico_moves(all_possible_moves)
            print(dico)
            lst_dico = []
            for element in dico:
                lst_dico.append(element)
            new_position = random.choice(lst_dico)
            old_position = dico[new_position]

            for pos in L_around_enemy_queen:
                if pos in potential_monkey_moves and ispossible(pos, potential_moves):
                    dico = dico_moves(all_possible_moves)
                    old_position = dico[pos]
                    new_position = pos
                if pos in potential_enemy_moves:
                    L_around_enemy_queen.remove(pos)  # Monkeys avoid danger

        for possibility in range(len(potential_enemy_monkey_moves)):
            if potential_enemy_monkey_moves[possibility] in your_monkey_position and \
                    ispossible(potential_enemy_monkey_moves[possibility], potential_moves):
                old_position = your_monkey_position[
                    your_monkey_position.index(potential_enemy_monkey_moves[possibility])]
                new_position = potential_enemy_monkey_moves[possibility]

    if new_position == Vec2I(None, None):
        new_position = random.choice(potential_moves)

    move_command = Command(old_position, new_position)
    board.play_command(move_command)
    return old_position, new_position


def dico_moves(ts_mouv_possibles):
    dico = {}
    for m in range(len(ts_mouv_possibles)):
        dico[ts_mouv_possibles[m][1]] = ts_mouv_possibles[m][0]  # pt d'arrivée : pt de départ
    return dico


def ispossible(position, posmoves):
    possible = True
    if position not in posmoves:
        possible = False
    return possible