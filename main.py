import os
import itertools
from Game import Game
from AI import AI


if __name__ == "__main__":
    possible = ['u', 'e', 'g']
    heuristics = [''.join(p) for p in itertools.permutations(possible)]
    runs = 1000
    filename = f"data/results_{heuristics[0]}_{runs}.csv"
    for h in heuristics:
        for i in range(runs):
            game = Game(4)
            ai = AI(game, h + 'r')

            while True:
                message = ai.ChooseBestMove()
                if message == "Won":
                    # winning logic
                    break
                if message == "Lost":
                    # losing logic
                    break

            if not os.path.exists(f'{filename}'):
                with open(f'{filename}', 'w') as f:
                    f.write('heuristic,max,score,message\n')

            with open(f'{filename}', 'a') as f:
                f.write(f'{h}, {game.max}, {game.official_score}, {message}\n')
