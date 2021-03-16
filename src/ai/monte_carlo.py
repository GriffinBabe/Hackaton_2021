import random
import math
from src.game.entities import Team


def next_coup(root):
    """
    :return: next coup with highest value
    """
    max_ = root.children[0]
    for elem in root.children:
        print(elem.val / elem.visits)
        if (elem.val / elem.visits) > (max_.val / max_.visits):
            max_ = elem
    print("max", (max_.val / max_.visits))
    return max_.coup_played


class MonteCarloTree:
    def __init__(self, num, game_interface, parent):
        self.num = num  # current player, necessary argument to determine to win value (-1 or 1)
        self.game_interface = game_interface
        self.parent = parent  # parent node
        self.children = []  # list of children nodes
        self.val = 0  # Cumulative value of win/loss encountered from this node
        self.ucb = 0  # Upper Confidence Bound
        self.visits = 0  # number of time this node has been visited during backup phase
        self.coup_played = None  # coup corresponding to this node
        self.next_win = False  # true if next coup is winning

    def update_ucb(self):
        # TODO : recheck UCB sigmoid formula with other sources
        mean_node_value = self.val / self.visits
        arg = math.log(self.parent.visits / self.visits)
        self.ucb = mean_node_value + 10 * math.sqrt(arg)

    def expansion(self):
        """
        expansion phase : randomly select a leaf (not visited yet)
        """
        win, pwin = self.game_interface.check_win()
        if pwin is None and self.next_win is False:
            coup = self.game_interface.list_plays(self.num)  # all next possible coup
            remaining_coup = coup.copy()  # list of next possible coup not already explored
            for elem in self.children:
                if elem.coup_played in coup:  # if coup already done, remove from possible coups
                    remaining_coup.remove(elem.coup_played)
            n_coup = random.choice(remaining_coup)

            next_C4G = self.game_interface.branch_play(n_coup)
            next_child = MonteCarloTree(Team.WHITE if self.num == Team.BLACK else Team.BLACK, next_C4G, self)
            next_child.coup_played = n_coup
            self.children.append(next_child)

            next_child.backup(next_child.rollout())
        elif pwin is not None:
            if self.parent is not None:
                self.parent.children = [self]  # if the coup is a winning coup, no need to explore the siblings of this coup
                self.parent.next_win = True # set a flag to indicate that the next coup of the parent is winning
            if pwin == self.num:
                self.backup(1)
            else:
                self.backup(-1)
        elif self.next_win is not None: # if the next coup is a winning one, no need to expanse to siblings
            if self.children[0].game_interface.check_win() == self.num:
                self.children[0].backup(1)
            else:
                self.children[0].backup(-1)

    def selection(self):
        """
        selection phase : select (recursively) the children with the best UCB until finding node with leaf(s)
        """
        best_ = random.choice(self.children)
        for elem in self.children:
            elem.update_ucb()
            if elem.ucb > best_.ucb:
                best_ = elem
        best_.tree_search()

    def rollout(self):
        """
        simulation phase : simulate random-coup game until one player win
        :return: 1 if current player win, -1 else
        """

        random_winner = self.game_interface.play_random_moves()
        if random_winner == self.num:
            return 1
        else:
            return -1

    def backup(self, result):
        """
        backup phase : go from leaf to root and update values at each node encountered
        :param result: win value from the simulation
        """
        self.visits += 1
        self.val += result

        if self.parent is not None:
            self.parent.backup(result)

    def tree_search(self):
        """
        Starts one iteration of MCT : selection recursively if possible, else expansion
        """
        if len(self.children) < len(self.game_interface.list_plays(self.num)):  # if unexplored children exist, expands
            self.expansion()
        elif len(self.children) > 0:
            self.selection()
        else:  # if leaf and no possible children
            self.backup(self.rollout())
