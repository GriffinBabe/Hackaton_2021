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
	Your AI entry point. This function gets called every time your AI is asked to make a play.
	The parameters contains all the information you need to picture the game state.

	The given lists of entities, queen information, etc... are a deep copy of the current game state, so don't try
	changing values there as this won't impact the game :p

	The execution time of this function is taken into account at each move, and a time limit is given to each team.

	:param board: the whole game state

	:param your_team: your team. Either Team.WHITE or Team.BLACK

	:param last_move: a tuple of two Vec2I (Vec2I(x_from, y_from), Vec2I(x_to, y_to)) of your opponent's last move.
	None if you are doing the first game move.

	:return: two objects Vec2I, Vec2I. The first object is the position of the piece you want to move, the second
	"""
	
	# There are only two teams, either Team.WHITE or Team.BLACK
	enemy_team = None
	if your_team == Team.WHITE:
		enemy_team = Team.BLACK
	else:
		enemy_team = Team.WHITE
	# ~ print("Team:", your_team)


	all_possible_moves = board.get_legal_moves(your_team)

	list_of_safe_moves = []
	entities = board.get_entities()
	my_queen = board.search_queen(your_team)
	optimal_move = check_can_eat_queen(board, all_possible_moves, enemy_team)

	list_of_safe_moves = find_safe_move(all_possible_moves, entities, enemy_team)

	list_of_safe_moves_for_queen = []
	list_of_move_to_eat_enemy = []
	for move in list_of_safe_moves:
		if move[0] == board.search_queen(your_team).get_position():
			list_of_safe_moves_for_queen.append(move)


	for move in all_possible_moves:
		for entity in entities: # can eat someone
			if move[1] == entity.get_position() and entity.get_team() == enemy_team:
				if is_safe(move[1], entities, enemy_team, move[1]):
					list_of_move_to_eat_enemy.append(move)


	entities = board.get_entities()
	#Iterate over all entities

	if optimal_move != (): # can eat the queen
		selected_move = optimal_move
		# ~ print("Optimal move eat queen:", optimal_move)
	elif len(list_of_move_to_eat_enemy) > 0:  # can eat an enemy
		# ~ print("MIAM MIAM MIAM", list_of_move_to_eat_enemy)
		selected_move = get_farthest_destination(list_of_move_to_eat_enemy)
	elif len(list_of_safe_moves_for_queen) > 0:
		# ~ print("MOVES QUEEN SAFELY")
		# ~ selected_move = random.choice(list_of_safe_moves_for_queen)
		moves_avoid_own_team = find_safe_move(list_of_safe_moves_for_queen, entities, your_team)
		# ~ print(list_of_safe_moves_for_queen)
		# ~ print(moves_avoid_own_team)
		if len(moves_avoid_own_team) > 0:
			# ~ print("CHOOSE MOVE AVOIDING OWN TEAM")
			selected_move = get_farthest_destination(moves_avoid_own_team)
		else:
			selected_move = get_farthest_destination(list_of_safe_moves_for_queen)
	elif len(list_of_safe_moves) > 0:
		# ~ print("NO SAFE MOVE FOR THE QUEEN")
		# ~ print(list_of_safe_moves)
		selected_move = random.choice(list_of_safe_moves)
	else:
		# ~ print("NO SAFE MOVE FOUND CHOOSING FROM RANDOM")
		selected_move = random.choice(all_possible_moves)
	# ~ print("SELECTED MOVE:", selected_move)
	return selected_move




def is_safe(arrival_pos, entities, team_to_avoid, start):
	safe = True
	# ~ if my_queen.get_position() == move[0]:  # check if it's the queen
	for entity in entities:
		if entity.get_position() != start and entity.get_team() == team_to_avoid:
			enemy_pos = entity.get_position()
			#				print("enemy_pos", enemy_pos)
			# ~ print("destination", destination)
			# ~ print("entity_pos", enemy_pos)
			# ~ print(entity.get_position())
			if enemy_pos.x == arrival_pos.x:
				# ~ print("Monkey on X", enemy_pos, destination)
				safe = False
			elif enemy_pos.y == arrival_pos.y:
				# ~ print("Monkey on Y", enemy_pos, destination)
				safe = False
			# Check la diagonale aussi
			elif abs(enemy_pos.x - arrival_pos.x) == abs(
					enemy_pos.y - arrival_pos.y):
				# ~ print("Monkey on diagonal", enemy_pos, destination)
				safe = False
	return safe

def find_safe_move(all_possible_moves, entities, team_to_avoid):
	res = []
#	print("all_possible_moves", all_possible_moves)
	for move in all_possible_moves:
		if is_safe(move[1], entities, team_to_avoid, move[0]):
			res.append(move)
	return res


def check_can_eat_queen(board, all_possible_moves, enemy_team):
	for move in all_possible_moves:
		destination = move[1]
		if destination == board.search_queen(enemy_team).get_position():
			# ~ print("CAN EAT QUEEN", move)
			return move
	return ()

def get_farthest_destination(list_of_moves):
	distance = 0
	res = ()
	for move in list_of_moves:
		temp_distance = abs(move[0].x - move[1].x) + abs(move[0].y - move[1].y)
		if temp_distance > distance:
			distance = temp_distance
			res = move
	# ~ print("Final:", res, distance)
	return res

	"""# a list containing all the entities from all the teams (either Monkeys or Queens)
	entities = board.get_entities()

	# just like entities, but into a map (dictionary). The key is a Vec2I object containing the position where you
	# want to get the entity. Use entity_map.get(Vec2I(x, y)) instead of entity_map[Vec2I(x, y)] if you want to avoid
	# raising a KeyError. Vec2I is used for the positions
	entity_map = board.get_entity_map()

	# List all the possible legal moves
	all_possible_moves = board.get_legal_moves(your_team)

	# You can iterate over all the entities like so:
	for entity in entities:
		position = entity.get_position()
		team = entity.get_team()
		print('Entity at position {}, is from team {}'.format(position, team))

	# You can get other information from the board functions.
	your_queen = board.search_queen(your_team)

	# There are only two teams, either Team.WHITE or Team.BLACK
	enemy_team = None
	if your_team == Team.WHITE:
		enemy_team = Team.BLACK
	else:
		enemy_team = Team.WHITE

	# you can do the same with this one liner
	enemy_team = Team.WHITE if your_team == Team.BLACK else Team.BLACK

	# get the enemy queen info from the board
	enemy_queen = board.search_queen(enemy_team)

	# Get the position of an entity, for example, with this queen
	# This can also work with Monkeys
	your_queen_position = enemy_queen.get_position()

	# Get the queen stack (number of remaining monkeys)
	your_queen_stack = your_queen.get_stack()

	# Print the position information, positions use the object Vec2I, defined in the file src/game/geo.py
	print(your_queen_position.x, your_queen_position.y)

	# Get all the possible moves for your queen
	possible_moves = your_queen.get_legal_moves()

	# We want to move our queen one cell down
	your_queen_x = your_queen_position.x
	your_queen_y = your_queen_position.y

	# Again, the game uses the Vec2I object for the positions
	new_position = Vec2I(your_queen_x, your_queen_y + 1)

	# As the board is a DEEP COPY of the real board, you can use it to forecast the future, for example, if you
	# want to list all your enemy moves after the move you want to select

	# As said, you have to return a tuple of Vec2I from this function, but to make a play you have to put those
	# two Vec2I in a Command object
	move_command = Command(your_queen_position, new_position)

	# Make a copy of the current game state
	current_board = board.copy_state()

	# Plays the command, now the board is just like you have played your decised move
	board.make_play(move_command)

	# Forecast all the legal moves from your opponent
	opponent_possible_responses = board.get_legal_moves()

	# We check if the new position is a legal move
	if new_position in possible_moves:
		# We make this play by returning the new_position
		return your_queen_position, new_position
	else:
		new_position = random.choice(possible_moves)
		return your_queen_position, new_position
	 """
