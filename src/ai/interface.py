"""
Interface files containing the functions necessary to run the AI on the game
"""
from abc import abstractmethod, ABC
from src.game.board import Board
from src.game.entities import Team
from src.game.command import Command
import random


class GameInterface(ABC):
    """
    Game Interface base class used to adapt the Monte Carlo Tree Search to any game
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def make_play(self, play):
        """
        Makes a play, updating the game state. Unlike branch_play, this method doesn't apply the updates state in a
        new deepcopy of the interface. This method is used to perform the real play.
        :param play: The play to make, a play can be found in the list returned from list_plays() method
        """
        pass

    @abstractmethod
    def branch_play(self, play):
        """
        Makes a play and returns a copy of a game interface object, with updated game state.
        :param play: the play to make, returned by the list_plays() method.
        :return: a copy of a game interface object, with updated game state
        """
        pass

    @abstractmethod
    def list_plays(self):
        """
        Lists all the possible plays, actionable by the function
        :return: a list of all possible plays
        """
        pass

    @abstractmethod
    def check_win(self):
        """
        Returns True if the game has finished, else false.
        Also returns which player has won if the game is over.
        :return: True/False, Player/None tuple.
        """
        pass

    @abstractmethod
    def play_random_moves(self):
        """
        Play random moves until the game has finished, then returns which player has won. Returns None if draw.
        :return: Winning player.
        """
        pass


class MonkeyQueenGameInterface(GameInterface):

    def __init__(self, team, board):
        super().__init__()
        self._team = team
        self._game = board

    def make_play(self, play):
        self._game.play_command(play)

    def list_plays(self):
        legal_commands = []
        legal_moves = self._game.get_legal_moves(self._team)
        for move_pair in legal_moves:
            legal_commands.append(Command(move_pair[0], move_pair[1]))
        return legal_moves

    def branch_play(self, play):
        new_state = self._game.copy_state()

        new_interface = MonkeyQueenGameInterface(team=self._team, board=new_state)
        new_interface.make_play(play)

        return new_interface

    def check_win(self):
        if self._game.game_over():
            return True, self._game.get_winner()
        else:
            return False, None

    def play_random_moves(self):
        while not self._game.game_over():
            possible_moves = self._game.get_legal_moves()
            selected_move = random.choice(possible_moves)
            self.make_play(selected_move)
        return self.check_win()


