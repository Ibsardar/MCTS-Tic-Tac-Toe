# -------------------------------------------------- #
# Filename:     TicTacToe.py
# Author:       Ibrahim Sardar
# Created:      09/12/2019
# Desc:         Main TicTacToe game class.
# -------------------------------------------------- #

# imports
from random import randint
from copy import deepcopy as copy

# macros
flipcoin = lambda: randint(1, 2)

# class
class TicTacToe:
    """ TicTacToe Game!

        This class controls the following:
        - player turns
        - win/lose/draw events
        - board updating
        - board rendering

        stores the following:
        - players
        - board
        - who goes first
        - game summary
    """

    def __init__(self, p1, p2):
        """ Initializes the game.
        """

        p1.play_index = 1
        p2.play_index = 2
        p1.opponent = p2
        p2.opponent = p1
        self.p1 = p1
        self.p2 = p2
        self.board = [
            ['_', '_', '_'],
            ['_', '_', '_'],
            ['_', '_', '_']
        ]
        self.go_first = flipcoin()
        self.turns = 0
        self.summary = 'Initialized.'

    def __str__(self):
        """ Replaces default print behaviour with a summary.
        """

        return self.summary

    def at(self, pt, board=None):
        """ Returns the value on the board at
            a point [x,y].
            
            * An alternate board may be passed instead as well. *
        """

        board = board
        if board is None:
            board = self.board

        return board[pt[1]][pt[0]]

    def set_at(self, pt, val, board=None):
        """ Sets the value on the board at
            a point [x,y].
            
            * An alternate board may be passed instead as well. *
        """

        board = board
        if board is None:
            board = self.board

        board[pt[1]][pt[0]] = val

    def next(self):
        """ Returns next player based on # of turns and who went 1st.
        """

        odd = self.turns % 2

        if odd == 0:
            if self.go_first == 1:
                return self.p1
            else:
                return self.p2
        else:
            if self.go_first == 1:
                return self.p2
            else:
                return self.p1

    def curr(self):
        """ Returns current player based on # of turns and who went 1st.
        """

        odd = self.turns % 2

        if odd == 0:
            if self.go_first == 1:
                return self.p2
            else:
                return self.p1
        else:
            if self.go_first == 1:
                return self.p1
            else:
                return self.p2
        
    def check(self, player, board=None):
        """ Checks game board for game state change:
            - 0 : nothing
            - 1 : current player wins
            - 2 : current player loses
            - 3 : draw
            
            * An alternate board may be passed instead as well. *
        """

        board = board
        if board is None:
            board = self.board

        # check horizontal wins
        for row in board:
            if (row[0] == player.symbol and
                row[1] == player.symbol and
                row[2] == player.symbol):
                return 1
            if (row[0] == player.opponent.symbol and
                row[1] == player.opponent.symbol and
                row[2] == player.opponent.symbol):
                return 2

        # check vertical wins
        for col in range(3):
            if (board[0][col] == player.symbol and
                board[1][col] == player.symbol and
                board[2][col] == player.symbol):
                return 1
            if (board[0][col] == player.opponent.symbol and
                board[1][col] == player.opponent.symbol and
                board[2][col] == player.opponent.symbol):
                return 2

        # check positive diagonal wins
        if (board[2][0] == player.symbol and
            board[1][1] == player.symbol and
            board[0][2] == player.symbol):
            return 1
        if (board[2][0] == player.opponent.symbol and
            board[1][1] == player.opponent.symbol and
            board[0][2] == player.opponent.symbol):
            return 2

        # check negative diagonal wins
        if (board[0][0] == player.symbol and
            board[1][1] == player.symbol and
            board[2][2] == player.symbol):
            return 1
        if (board[0][0] == player.opponent.symbol and
            board[1][1] == player.opponent.symbol and
            board[2][2] == player.opponent.symbol):
            return 2

        # check for draw
        not_draw = False
        for row in board:
            if not_draw:
                break
            for symbol in row:
                if symbol is '_':
                    not_draw = True
                    break
        if not_draw is False:
            return 3

        # no game state change required
        return 0

    def moves(self, board=None):
        """ Returns a list of possible moves (positions).
            
            * An alternate board may be passed instead as well. *
        """

        if board is None:
            board = self.board

        moves = []

        for j in range(len(board)):
            row = board[j]
            for i in range(len(row)):
                if row[i] is '_':
                    moves.append([i,j])

        return moves

    def cheap_copy(self):
        """ Returns a copy of the game board.
        """

        return copy(self.board)

    def render(self):
        """ Prints the board using text.
        """

        b = self.board

        s = '\n'
        s += '\t {} | {} | {} \n'.format(b[0][0], b[0][1], b[0][2])
        s += '\t---+---+---\n'
        s += '\t {} | {} | {} \n'.format(b[1][0], b[1][1], b[1][2])
        s += '\t---+---+---\n'
        s += '\t {} | {} | {} \n'.format(b[2][0], b[2][1], b[2][2])

        print(s)

    def start(self, debug=False, detail=False):
        """ Begins and manages the game.
        """

        print("Game has started...\n")

        self.summary = 'Game started.'
        complete = False
        current = None
        while not complete:

            # next turn
            self.turns += 1

            # next player
            current = self.curr()
            self.summary = "It is currently Player " + str(current.play_index) + "'s turn. (" + current.symbol + ")"

            # if 1st turn, set symbols (affects both players)
            if (self.turns == 1):
                current.choose_symbol()

            # render board
            self.render()
            print("Player " + str(current.play_index) + "'s turn (" + current.symbol + "):")
            
            # current player picks move (bad moves handled inside 'go')
            move = current.go(self, debug, detail)
            if move is None:
                print("MCTS ran out of time and was not able to find any moves... turn skipped!")
                continue
            self.board[move[1]][move[0]] = current.symbol

            # check & handle events
            # 0 : nothing
            # 1 : current player wins
            # 2 : current player loses
            # 3 : draw
            state = self.check(current)
            if state is not 0:
                complete = True
                if state is 1:
                    self.summary = "Game over. Player " + str(current.play_index) + " (" + current.symbol + ") wins!"
                elif state is 2:
                    self.summary = "Game over. Player " + str(current.opponent.play_index) + " (" + current.symbol + ") wins!"
                elif state is 3:
                    self.summary = "Game over. It is a draw."
        
        self.render() # final render

        

