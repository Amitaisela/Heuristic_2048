import numpy as np


class Game:
    def __init__(self, size):
        self.current_state = np.array(
            [[0 for _ in range(size)] for _ in range(size)])
        self.official_score = 0
        self.max = 0

        self.__init_board(size)

    def __init_board(self, size):
        coord1 = (np.random.randint(0, size), np.random.randint(0, size))
        coord2 = (np.random.randint(0, size), np.random.randint(0, size))

        init_numbers_one = np.random.choice([2, 4])
        init_numbers_two = np.random.choice([2, 4])
        self.max = max(init_numbers_one, init_numbers_two)
        while coord1 == coord2:
            coord2 = (np.random.randint(0, size), np.random.randint(0, size))

        self.current_state[coord1[0]][coord1[1]] = init_numbers_one
        self.current_state[coord2[0]][coord2[1]] = init_numbers_two

    def copy(self):
        game = Game(len(self.current_state))
        game.official_score = self.official_score
        game.max = self.max

        for i in range(len(self.current_state)):
            for j in range(len(self.current_state)):
                game.current_state[i][j] = self.current_state[i][j]
        return game

    def __str__(self):
        board = ""
        for row in self.current_state:
            board += "+------+------+------+------+\n"
            board += "| " + " | ".join(
                f"{cell:^4}" for cell in row
            ) + " |\n"
        board += "+------+------+------+------+\n"
        board += f"Score: {self.official_score}\n"
        return board

    def update(self, move, matrix, score):
        self.current_state = matrix
        self.official_score += score
        self.max = max(self.max, np.max(self.current_state))

        emptyCells = self.emptyCells()
        if len(emptyCells) > 0:
            newNumber = 2 if np.random.random() < 0.9 else 4
            newCell = emptyCells[np.random.choice(range(len(emptyCells)))]
            self.current_state[newCell[0]][newCell[1]] = newNumber

    def getNextMoves(self):
        moves = {}
        for move, matrix in self.generateRotations().items():
            merged_matrix, score = self.merge_upwards(matrix)

            if move == 'up':
                # rotate back to original
                moves[move] = (merged_matrix, score)
            elif move == 'left':
                # rotate back to original
                moves[move] = (self.rotate_matrix(merged_matrix, 270), score)

            elif move == 'down':
                # rotate back to original
                moves[move] = (self.rotate_matrix(merged_matrix, 180), score)

            elif move == 'right':
                # rotate back to original
                moves[move] = (self.rotate_matrix(merged_matrix, 90), score)

        # Check if there are any changes, keep only the moves that changed the board

        for move, (matrix, score) in list(moves.items()):
            if np.array_equal(matrix, self.current_state):
                del moves[move]

        return moves

    def merge_upwards(self, matrix):
        size = len(matrix)
        merged_matrix = np.zeros((size, size), dtype=int)
        score = 0

        for col in range(size):
            # Extract the column and filter out zeros
            column = [matrix[row][col]
                      for row in range(size) if matrix[row][col] != 0]
            merged_column = []
            skip = False

            # Merge tiles
            for i in range(len(column)):
                if skip:
                    skip = False
                    continue
                if i < len(column) - 1 and column[i] == column[i + 1]:
                    # Merge tiles
                    merged_value = column[i] * 2
                    merged_column.append(merged_value)
                    score += merged_value
                    skip = True
                else:
                    merged_column.append(column[i])

            # Fill the rest with zeros
            while len(merged_column) < size:
                merged_column.append(0)

            # Place the merged column back into the matrix
            for row in range(size):
                merged_matrix[row][col] = merged_column[row]

        return merged_matrix, score

    def rotate(self, command: str):
        command = command.lower()

        if command == 'up':
            return self.current_state, True

        elif command == 'left':
            rotated = self.rotate_matrix(self.current_state, 90)
            return rotated, True

        elif command == 'down':
            rotated = self.rotate_matrix(self.current_state, 180)
            return rotated, True

        elif command == 'right':
            rotated = self.rotate_matrix(self.current_state, 270)
            return rotated, True

        return self.current_state, False

    def rotate_matrix(self, matrix, degrees):
        degreeList = [90, 180, 270, 360]
        if degrees not in degreeList:
            raise ValueError(
                f"Degrees must be {degreeList}.\nGotten {degrees}")

        def rotate_90(matrix):
            return [list(row[::-1]) for row in zip(*matrix)]

        if degrees == 90:
            return rotate_90(matrix)
        elif degrees == 180:
            return rotate_90(rotate_90(matrix))
        elif degrees == 270:
            return rotate_90(rotate_90(rotate_90(matrix)))
        elif degrees == 360 or degrees == 0:
            return matrix

    def generateRotations(self):
        possibleRotations = {}
        for direction in ['up', 'left', 'down', 'right']:
            rotated, valid = self.rotate(direction)
            if valid:
                possibleRotations[direction] = rotated

        return possibleRotations

    def emptyCells(self):
        emptyCells = []
        for i in range(len(self.current_state)):
            for j in range(len(self.current_state[i])):
                if self.current_state[i][j] == 0:
                    emptyCells.append((i, j))
        return emptyCells
