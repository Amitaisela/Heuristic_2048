import os
import itertools
from Game import Game
from AI import AI
import math


if __name__ == "__main__":
    possible = ['m', 'u', 'e', 'g']
    heuristics = [''.join(p) for p in itertools.permutations(possible)]
    runs = 1000
    for h in heuristics:
        for i in range(runs):
            game = Game(4)
            ai = AI(game, h + 'r')

            while True:
                message = ai.ChooseBestMove()
                if message == "Won":
                    break
                if message == "Lost":
                    break

            if not os.path.exists(f'results_{runs}.csv'):
                with open(f'results_{runs}.csv', 'w') as f:
                    f.write('heuristic,max,score,message\n')

            with open(f'results_{runs}.csv', 'a') as f:
                f.write(f'{h}, {game.max}, {game.official_score}, {message}\n')
