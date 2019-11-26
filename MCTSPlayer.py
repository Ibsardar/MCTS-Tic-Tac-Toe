# -------------------------------------------------- #
# Filename:     MCTSPlayer.py
# Author:       Ibrahim Sardar
# Created:      09/12/2019
# Desc:         Main Monte-Carlo Tree Search
#               Simulator AI-player class.
# -------------------------------------------------- #

# imports
import random
import math
from MonteCarloTree import MonteCarloTree

# constants
SQRT2 = math.sqrt(2)

# class
class MCTSPlayer:
    """ Monte-Carlo Tree Search TicTacToe AI Player!

        This class does the following:
        - selects a move based on board data via mcts
        - selects initial symbols if invoked
        
        * mcts process limited to 1 second by default *
    """

    def __init__(self, time_limit=1000, explore_importance=SQRT2):
        """ Initializes the ai.
        """

        self.play_index = 0
        self.symbol = '?'
        self.opponent = None
        self.time_limit = time_limit
        self.uct_c = explore_importance

    def choose_symbol(self):
        """ (Invoked if winner of initialcoin flip)
        
            Randomly select a symbol for self.
            (Also set opponent's to the opposite symbol)
        """

        print("Player " + str(self.play_index) + " wins the coin flip!")
        print("Player " + str(self.play_index) + ", choose a symbol: X, O")

        self.symbol = random.choice(['X', 'O'])
        if self.symbol == 'X':
            self.opponent.symbol = 'O'
        elif self.symbol == 'O':
            self.opponent.symbol = 'X'

        print("Player " + str(self.play_index) + " chooses " + self.symbol + "!")
        print("Player " + str(self.opponent.play_index) + "'s symbol is " + self.opponent.symbol + ".")

    def go(self, game, debug=False, detail=False):
        """ Uses mcts to pick the next best move.
        """

        tree = MonteCarloTree.search(
            game = game,
            time_limit = self.time_limit,
            uct_const = self.uct_c,
            dbg = debug,
            dtl = detail
        )

        return tree.best_move(debug)

        
