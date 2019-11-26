# -------------------------------------------------- #
# Filename:     MonteCarloTree.py
# Author:       Ibrahim Sardar
# Created:      09/12/2019
# Desc:         Monte Carlo Tree class used for mcts.
# -------------------------------------------------- #

# imports
import time
import random
import math
from copy import deepcopy as copy
from MonteCarloNode import MonteCarloNode

# constants
# change these if you know what you are doing
WIN_SCORE  = 1.0
DRAW_SCORE = 0.5
LOSE_SCORE = 0.0
# don't change these
OUTCOME_NONE = 0
OUTCOME_WIN  = 1
OUTCOME_LOSE = 2
OUTCOME_DRAW = 3

# macros
now = lambda: int(round(time.time() * 1000)) # in milliseconds

# class
class MonteCarloTree:
    """ Monte-Carlo Tree!

        This class does the following:
        - searches via MCTS algorithm
        
        * search is a static method *
        * the tree itself is returned from the search *
        * making a tree by itself is NOT useful *
    """

    def __init__(self, player, state, dtl=False):
        """ Initializes the a monte-carlo tree.
        """

        self.root = MonteCarloNode(
            player      = player.opponent, # 1st state is of current player's opponent
            state       = copy(state), # we don't want to edit the actual game board!
            parent      = None,
            move        = None, # can ignore move, if any, which got us to the root node
            wins        = 0, # how many wins this node got in mcts so far
            sims        = 0, # how many simulations this node played out so far
            children    = [] # list of child nodes as a result of different possible moves taken
        )

        self.dtl = dtl # for debugging

    def __str__(self):
        """ Replaces default print behavior by printing  tree node data
        """

        s = '\n'
        s += 'Monte Carlo Tree:\n'
        s += self.root._to_str(self.dtl, '    ')
        return s

    def best_move(self, dbg):
        """ Returns the next best move. If no moves
            left, returns None.
        """

        most_wins = -math.inf
        bestt_child = None
        wins_lst = []
        move_lst = []
        
        for child in self.root.c:
            wins = child.wins
            if dbg:
                wins_lst.append(wins)
                move_lst.append(child.move)
            if most_wins < wins:
                most_wins = wins
                best_child = child

        if dbg:
            print("Final move selection:")
            for i in range(len(wins_lst)):
                w = wins_lst[i]
                m = move_lst[i]
                print("Score = " + str(w) + " for move: " + str(m))
            print("Best move: " + str(best_child.move))

        if best_child is None:
            return None

        return best_child.move

    def best_child(self, n, C, dtl=False):
        """ Returns the maximum-UCT scoring child from node 'n'
        """

        # init vars
        max_pts = -math.inf
        max_pts_child = None
        children = n.c

        scors = []
        moves = []

        # search children
        for child in children:
            pts = MonteCarloTree._UCT(child, C)
            if dtl:
                scors.append(pts)
                moves.append(child.move)
            if max_pts < pts:
                max_pts = pts
                max_pts_child = child

        if dtl:
            for i in range(len(scors)):
                s = scors[i]
                m = moves[i]
                print("UCT = " + str(s) + " for move: " + str(m))

        # if children exist AND
        # if all children have -infinity scores,
        # just return the 1st child:
        if max_pts_child is None:
            if n.amount():
                return n.c[0]

        # return biggest winner
        return max_pts_child

    @staticmethod
    def search(game, time_limit, uct_const, dbg=False, dtl=False):
        """ Static method:
            Runs the famous MCTS algorithm by creating a
            tree, running selection, expansion, simulation,
            and backpropagation on it, then after the time
            limit is reached, returns the tree.

            - 'game' is a TicTacToe game object
            - 'time_limit' is limit (ms) of mcts runtime
            - 'uct_const' is a constant that determines exploration
        """

        # setup tree
        tree = MonteCarloTree(game.curr(), copy(game.board), dtl)
        time_interval = 225 # for "thinking..." effect
        
        # search tree
        MonteCarloTree._select(
            game,
            tree,
            tree.root,
            uct_const,
            now() + time_limit, # end time
            now() - time_interval, # last time
            time_interval,
            dbg,
            dtl
        )

        # return tree
        return tree

    @staticmethod
    def _select(g, t, n, c, te, tl, intv, dbg, dtl):
        """ Scores the tree by selecting the best move every
            until the time limit is reached.
        """

        # prepare variables
        def debug(o):
            if dbg:
                print(o)
        debug("Preparing initial variables...")
        def SELECT(node):
            nonlocal n
            n.mcts_curr = False
            n = node
            n.mcts_curr = True
        EXPAND = MonteCarloTree._expand
        SIMULATE = MonteCarloTree._simulate
        BACKPROP = MonteCarloTree._backpropagate
        orig_player = g.curr()
        n.mcts_curr = True

        # search loop
        while True:

            # debugging
            debug(t)

            # check time
            debug("Checking time limit...")
            if tl + intv <= now():
                tl = now()
                print('Thinking...')
            if now() >= te:
                debug('Time limit reached!')
                return

            # prepare variables
            debug("Preparing variables...")
            curr_player = n.player.opponent
            curr_board = n.state

            # check state
            debug("Checking game state...")
            result = g.check(curr_player, curr_board)
            if result is not OUTCOME_NONE:
                if n is t.root:
                    debug("Final game state reached.")
                    continue
                else:
                    debug("Final game state reached, backpropagating...")
                    BACKPROP(n, result, woff=math.inf, loff=-math.inf)
                    SELECT(t.root)
                    continue

            # check # of simulations
            debug("Checking number of simulations...")
            sims = n.sims
            if sims is 0:
                if n is not t.root:
                    debug("No simulations found, simulating and backpropagating...")
                    sim_result = SIMULATE(g, n)
                    BACKPROP(n, sim_result)
                    SELECT(t.root)
                    continue

            # check # of children
            debug("Checking number of children...")
            number_of_children = n.amount()
            if number_of_children is 0:
                debug("No children found, expanding...")
                EXPAND(g, n)
                first_child = n.c[0]
                SELECT(first_child)
                continue
            
            # pick best UCT valued child
            else:
                debug("Children found, selecting highest probable child...")
                SELECT(t.best_child(n, c, dtl))
                continue

    @staticmethod
    def _expand(game, leaf):
        """ Create child nodes for every action.
        """

        # expand
        current_board = leaf.state
        moves = game.moves(current_board)
        for mv in moves:
            leaf.make_leaf(mv)

    @staticmethod
    def _simulate(game, leaf):
        """ Default random playout:
                Simulate the rest of the game randomly
                until end reached and return the result.

            * Expects that the leaf node has at least 1
              playable move. *
        """
        
        # prepare variables
        orig_player = leaf.player.opponent
        sim_player = leaf.player.opponent
        sim_board = copy(leaf.state)
        def move(mv):
            sim_board[mv[1]][mv[0]] = sim_player.symbol

        # simulation loop (random tic-tac-toe)
        while True:

            # simulate
            random_move = random.choice(game.moves(sim_board))
            move(random_move)

            # only stop if game ends
            result = game.check(orig_player, sim_board)
            if result is not OUTCOME_NONE:
                return result

            # move to next player
            sim_player = sim_player.opponent

    @staticmethod
    def _backpropagate(leaf, result, woff=0, loff=0, doff=0):
        """ Updates nodes in path from leaf node to root.

            * One-time offsets are also available for each
              type of result. (will only be applied once in
              recursion sequence) *
        """
        
        # prepare variables
        curr_node = leaf
        team_orig = leaf.player.opponent.play_index
        team = lambda n: n.player.play_index
        parent = lambda n: n.p
        
        # backpropagate:
        while curr_node is not None:

            # increment simulations (i.e. visits)
            curr_node.sims += 1

            # increment wins if current node is on the same team as the original node
            if result is OUTCOME_WIN:
                if team(curr_node) is team_orig:
                    curr_node.wins += WIN_SCORE + woff
                else:
                    curr_node.wins += LOSE_SCORE + loff

            # opposite of above
            if result is OUTCOME_LOSE:
                if team(curr_node) is team_orig:
                    curr_node.wins += LOSE_SCORE + loff
                else:
                    curr_node.wins += WIN_SCORE + woff

            # draws do not depend on team
            if result is OUTCOME_DRAW:
                curr_node.wins += DRAW_SCORE + doff

            # clear offsets
            woff = loff = doff = 0

            # backtrack
            curr_node = parent(curr_node)

    @staticmethod
    def _UCT(node, explore_constant):
        """ Upper Confidence Bounds for Trees formula.
            Maintains a balance between exploration
            and exploitation.
            
            * Only meant for nodes with a parent! *
        """

        w = node.wins
        s = node.sims
        N = node.p.sims
        C = explore_constant

        ln = lambda x: math.log(x)
        sqrt = lambda x: math.sqrt(x)

        if s == 0:
            return math.inf
        else:
            return (w / s) + (C * sqrt(ln(N) / s))