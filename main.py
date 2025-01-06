import os
import itertools
from Game import Game
from AI import AI
import math


if __name__ == "__main__":
    possible = ['m', 'u', 'e', 'g']
    heuristics = [''.join(p) for p in itertools.permutations(possible)]
    runs = math.comb(16, 2)*2
    for h in heuristics:
        for i in range(runs):
            game = Game(4)
            ai = AI(game, h + 'r')
            # print(game)

            while True:
                message = ai.ChooseBestMove()
                if message == "Won":
                    # print("You won!")
                    break
                if message == "Lost":
                    # print("You lost!")
                    break

                # os.system('cls' if os.name == 'nt' else 'clear')
                # print(ai.lastMove, "\n", game)

            # now save in a csv, add headers if it's the first time
            if not os.path.exists('results.csv'):
                with open('results.csv', 'w') as f:
                    f.write('heuristic,max,score,message\n')

            with open('results.csv', 'a') as f:
                f.write(f'{h}, {game.max}, {game.official_score}, {message}\n')
