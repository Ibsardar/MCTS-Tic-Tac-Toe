# -------------------------------------------------- #
# Filename:     MonteCarloNode.py
# Author:       Ibrahim Sardar
# Created:      09/12/2019
# Desc:         A Node class for the Monte Carlo Tree.
# -------------------------------------------------- #

# imports
from copy import deepcopy as copy

# class
class MonteCarloNode:
    """ Monte-Carlo Node!

        This class takes care of the following:
        - stores data related to MCTS algorithm
    """

    def __init__(self, player, state, parent=None, move=None, wins=0, sims=0, children=[]):
        """ Initializes the a monte-carlo tree.
        """

        self.player = player # the player who just made a move
        self.state = state # the board AFTER the player made a move
        self.p = parent # the node of the board BEFORE the player made a move
        self.move = move # the move player just made (to get to this state)
        self.wins = wins # number of times this player won in simulations
        self.sims = sims # number of times this player has played simulations
        self.c = copy(children) # list of states resulting from all possible moves the opponent can make
        self.mcts_curr = False # if this is the current node being processed in MCTS (for debugging)

        if parent:
            parent.c.append(self)

        if move:
            state[move[1]][move[0]] = player.symbol # apply a previous move

    def _to_str(self, detailed=False, prefix=""):
        """ Returns self's sub-tree in the form of a string
        """

        is_it = ""
        pfx = "" + prefix
        if self.mcts_curr:
            is_it = "=> "
            pfx = prefix[0:-3] + is_it

        s = pfx + "Node: w=" + str(self.wins) + " s=" + str(self.sims) + " mv=" + str(self.move) + " p=" + str(self.player.play_index)
        if detailed:
            s += '\n' + prefix + str(self.state[0]) + '\n' + prefix + str(self.state[1]) + '\n' + prefix + str(self.state[2])
        s += '\n'

        for child in self.c:
            s += child._to_str(detailed, prefix + prefix)

        return s

    def amount(self):
        """ Number of children.
        """

        return len(self.c)

    def make_leaf(self, move):
        """ Creates a leaf node given a move.
            Also returns the created node.
        """

        return MonteCarloNode(
            self.player.opponent,
            copy(self.state),
            self,
            move
        )
