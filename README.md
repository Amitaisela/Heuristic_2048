# 2048 Solver and Heuristics

## Reference Paper

The heuristics used in this project are inspired by the following paper:
["Composition of Basic Heuristics for the Game 2048"](https://theresamigler.com/wp-content/uploads/2020/03/2048.pdf)

## Heuristics Overview

### 1. **Greedy Heuristic**

- **Description**: Selects the state with the highest official score. The score is calculated as the sum of the tiles created by merging other tiles. For instance, when two 8 tiles merge into a 16 tile, 16 is added to the score.

### 2. **Empty Tile Heuristic**

- **Description**: Prioritizes states with the highest number of empty tiles, maximizing available space for future moves.

### 3. **Uniformity Heuristic**

- **Description**: Prefers states that produce the most tiles of the same value, aiming for uniformity.

### 4. **Monotonicity Heuristic**

- **Description**: Encourages states with high monotonicity. A state is considered monotonic if:
  - The tile values are non-increasing or non-decreasing along rows and columns.
  - The highest tile value is positioned in one of the four corners.

### 5. **Random Heuristic**

- **Description**: Selects a move randomly from the available options, providing variability.

## Approach to Solving 2048

In the game of 2048, states can appear visually distinct but represent similar strategies. To handle this:

1. Multiple heuristics are applied in sequence.
2. The random heuristic is used as a fallback to explore remaining options after narrowing down using other heuristics.

This multi-heuristic strategy allows for a more robust approach to solving the game.
