# -------------------------------------------------- #
# Filename:     test_mcts_ttt.py
# Author:       Ibrahim Sardar
# Created:      09/12/2019
# Desc:         Test MCTS AI with Tic Tac Toe.
# -------------------------------------------------- #

# imports
import os
from HumanPlayer import HumanPlayer
from MCTSPlayer import MCTSPlayer
from TicTacToe import TicTacToe

# testing harness
def main():

    # clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Intro
    print('Filename: \t"test_mcts_ttt.py"')
    print('Version:  \t1.0.0')
    print('Project:  \tMonte Carlo Tree Search Simulator with Tic Tac Toe')
    print('Author:   \tIbrahim Sardar')
    print('Date:     \t09/20/2019')
    print('Company:  \tFunai Service, OH, USA')
    print('Desc:     \tProgram showing how MCTS works using Tic Tac Toe.')
    print('\n\n')
    print('#########################/|\#######################')
    print('#####/---------------------------------------\#####')
    print('###<|   Monte Carlo Tree Search Simulator!    |>###')
    print('#####\--------\   with Tac Tac Toe   /-------/#####')
    print('###############\--------------------/##############')
    print('#########################\|/#######################')

    # Main program
    while True:
        print('\n\n\nPick Simulation:')
        print('0) Quit')
        print('1) [NOT AVAILABLE] Human vs Human')
        print('2) Human vs AI')
        print('3) AI vs AI')
        print('4) DEBUG: Human vs AI')
        print('5) DEBUG: AI vs AI')
        print('6) DEBUG: Human vs AI (DETAILED)')
        print('7) DEBUG: AI vs AI (DETAILED)')
        choice = int(input('Choice: '))

        if choice == 0:
            return
        elif choice == 1:
            print('NOT SUPPORTED YET.')
        elif choice == 2:
            player1 = HumanPlayer()
            player2 = MCTSPlayer()
            #player2.time_limit = 2500 # 2.5 sec
            #player2.uct_c = 2 # explore more than usual
            game = TicTacToe(player1, player2)
            print(game.summary)
            game.start()
            print(game.summary)
        elif choice == 3:
            player1 = MCTSPlayer()
            #player1.uct_c = 1
            #player1.time_limit = 10000
            player2 = MCTSPlayer()
            #player2.uct_c = 2
            #player2.time_limit = 10000
            game = TicTacToe(player1, player2)
            print(game.summary)
            game.start()
            print(game.summary)

        # DEBUGGING:
        elif choice == 4:
            player1 = HumanPlayer()
            player2 = MCTSPlayer()
            player2.time_limit = 1500
            game = TicTacToe(player1, player2)
            print(game.summary)
            game.start(debug=True)
            print(game.summary)
        elif choice == 5:
            player1 = MCTSPlayer()
            player2 = MCTSPlayer()
            player1.time_limit = 1500
            player2.time_limit = 1500
            game = TicTacToe(player1, player2)
            print(game.summary)
            game.start(debug=True)
            print(game.summary)
        elif choice == 6:
            player1 = HumanPlayer()
            player2 = MCTSPlayer()
            player2.time_limit = 2000
            # player2.uct_c = 2
            game = TicTacToe(player1, player2)
            print(game.summary)
            game.start(debug=True, detail=True)
            print(game.summary)
        elif choice == 7:
            player1 = MCTSPlayer()
            player2 = MCTSPlayer()
            player1.time_limit = 2000
            player2.time_limit = 2000
            game = TicTacToe(player1, player2)
            print(game.summary)
            game.start(debug=True, detail=True)
            print(game.summary)

# if this is file running, run the following
if __name__ == "__main__":
    main()
