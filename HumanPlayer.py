# -------------------------------------------------- #
# Filename:     HumanPlayer.py
# Author:       Ibrahim Sardar
# Created:      09/19/2019
# Desc:         Main Monte-Carlo Tree Search
#               Simulator human-player class.
# -------------------------------------------------- #

# class
class HumanPlayer:
    """ Monte-Carlo Tree Search TicTacToe Human Player!

        This class does the following:
        - allows human to select a move
        - allows human to select an initial symbol if invoked
    """

    def __init__(self):
        """ Initializes the ai.
        """

        self.play_index = 0
        self.symbol = '?'
        self.opponent = None

    def choose_symbol(self):
        """ (Invoked if winner of initialcoin flip)
        
            Human selects a symbol for self.
            (Also set opponent's to the opposite symbol)
        """

        print("Player " + str(self.play_index) + " wins the coin flip!")
        print("Player " + str(self.play_index) + ", choose a symbol: X, O")
        symbol = input('')
        if symbol is not 'O' and symbol is not 'X':
            print('Invalid symbol. Defaulted to X')
            symbol = 'X'

        self.symbol = symbol
        if self.symbol == 'X':
            self.opponent.symbol = 'O'
        elif self.symbol == 'O':
            self.opponent.symbol = 'X'

        print("Player " + str(self.play_index) + " chooses " + self.symbol + "!")
        print("Player " + str(self.opponent.play_index) + "'s symbol is " + self.opponent.symbol + ".")

    def go(self, game, debug=False, detail=False):
        """ Human selects x and y coordinates of next move.
        """

        move = None
        while True:

            print("Pick a position:")
            s = '\n'
            s += '\t a | b | c \n'
            s += '\t---+---+---\n'
            s += '\t d | e | f \n'
            s += '\t---+---+---\n'
            s += '\t g | h | i \n'
            print(s)

            choice = input("")

            if choice is "quit":
                return None

            if len(choice) != 1:
                print("Invalid choice. Try again...")
                continue
            
            asci = ord(choice)
            if asci < 97 or asci > 105:
                print("Invalid choice. Try again...")
                continue

            # quick function to convert
            # character to position:
            def conv(c):
                if c == 'a':
                    return [0,0]
                if c == 'b':
                    return [1,0]
                if c == 'c':
                    return [2,0]
                    
                if c == 'd':
                    return [0,1]
                if c == 'e':
                    return [1,1]
                if c == 'f':
                    return [2,1]
                    
                if c == 'g':
                    return [0,2]
                if c == 'h':
                    return [1,2]
                if c == 'i':
                    return [2,2]

            move = conv(choice)
            if game.at(move) is not '_':
                print("Invalid choice. Try again...")
                continue

            game.set_at(move, self.symbol)
            break

        return move

        
