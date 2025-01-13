from Game import Game
import random


class AI():
    def __init__(self, game_instance: Game, heuristic: str):
        self.game = game_instance
        self.heuristic = heuristic
        self.lastMove = None

    def ChooseBestMove(self):
        AIPlay = self.play()
        if AIPlay == True:
            return "Won"

        elif AIPlay == False:
            return "Lost"

        move = list(AIPlay.keys())[0]
        matrix = AIPlay[move][0]
        score = AIPlay[move][1]
        self.game.update(move, matrix, score)
        self.lastMove = move

        return "Moved"

    def play(self):
        possibleMoves = self.game.getNextMoves()

        if len(possibleMoves) == 0:
            if self.game.max == 2048:
                return True
            return False

        filteredMoves = possibleMoves
        for h in self.heuristic:
            filteredMoves = self.calculate_heuristic(filteredMoves, h)

            if len(filteredMoves) == 1:
                return filteredMoves

            if len(filteredMoves) > 1:
                continue

    def calculate_heuristic(self, possibleMoves, heuristic):
        if heuristic == 'm':
            return self.m(possibleMoves)
        elif heuristic == 'u':
            return self.u(possibleMoves)
        elif heuristic == 'e':
            return self.e(possibleMoves)
        elif heuristic == 'g':
            return self.g(possibleMoves)
        elif heuristic == 'r':
            return self.r(possibleMoves)

        else:
            raise ValueError(f"Heuristic {heuristic} not found")

    def u(self, possibleMoves: dict):
        uniformity_scores = {}
        for move, (matrix, _) in possibleMoves.items():
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    value = matrix[i][j]
                    currentValue = self.game.current_state[i][j]
                    if value != 0 and value != currentValue:
                        if move not in uniformity_scores:
                            uniformity_scores[move] = 0
                        uniformity_scores[move] += 1

        max_uniformity = max(uniformity_scores.values())

        # Return moves with the maximum uniformity score
        bestMoves = [move for move in uniformity_scores.keys(
        ) if uniformity_scores[move] == max_uniformity]
        bestStates = {move: possibleMoves[move] for move in bestMoves}

        return bestStates

    def m(self, possibleMoves: dict):
        def is_monotonic(sequence):
            return all(x >= y for x, y in zip(sequence, sequence[1:])) or all(x <= y for x, y in zip(sequence, sequence[1:]))

        def calculate_monotonicity(matrix):
            monotonicity_score = 0

            # Check monotonicity for rows
            for row in matrix:
                if is_monotonic(row):
                    monotonicity_score += 1

            # Check monotonicity for columns
            for col in zip(*matrix):
                if is_monotonic(col):
                    monotonicity_score += 1

            # Check if the maximum value is in a corner
            max_value = max(max(row) for row in matrix)
            corners = [matrix[0][0], matrix[0][-1],
                       matrix[-1][0], matrix[-1][-1]]
            if max_value in corners:
                monotonicity_score += 1

            return monotonicity_score

        monotonicity_scores = {}
        for move, (matrix, _) in possibleMoves.items():
            monotonicity_scores[move] = calculate_monotonicity(matrix)

        max_monotonicity = max(monotonicity_scores.values())

        bestMoves = [move for move, score in monotonicity_scores.items(
        ) if score == max_monotonicity]
        bestStates = {move: possibleMoves[move] for move in bestMoves}

        return bestStates

    def e(self, possibleMoves: dict):
        countEmpty = {}
        for move in possibleMoves.keys():
            matrix = possibleMoves[move][0]
            for row in matrix:
                for cell in row:
                    if cell == 0:
                        if move not in countEmpty:
                            countEmpty[move] = 1
                        else:
                            countEmpty[move] += 1

        maxValue = max(countEmpty.values())

        bestMoves = [move for move in countEmpty.keys()
                     if countEmpty[move] == maxValue]

        bestStates = {move: possibleMoves[move] for move in bestMoves}

        return bestStates

    def g(self, possibleMoves: dict):
        sum = {}
        for move in possibleMoves.keys():
            sum[move] = possibleMoves[move][1] + self.game.official_score

        maxValue = max(sum.values())

        bestMoves = [move for move in sum.keys()
                     if sum[move] == maxValue]

        bestStates = {move: possibleMoves[move] for move in bestMoves}

        return bestStates

    def r(self, possibleMoves: dict):
        move = random.choice(list(possibleMoves.keys()))
        bestStates = {move: possibleMoves[move]}

        return bestStates
