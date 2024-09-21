# Four in a Row Game

This is a Python implementation of the classic "Four in a Row" (also known as "Connect Four") game. It features a graphical user interface (GUI) and supports multiple AI agents using various algorithms. You can play against another human or challenge one of the AI agents.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Game Options](#game-options)
- [Agents](#agents)
- [Examples](#examples)
- [Running Analysis](#running-analysis)

## Installation

To run the game, ensure you have Python 3.x installed. 


## Usage

Run the game with the following command:

```bash
python3 main.py --agent1 <Agent1> --agent2 <Agent2> --display <DisplayType> [OPTIONS]
```

## Game Options
- `--random_seed`: Set the random state seed (default: random).
- `--display`: Choose the UI type:
  - `GUI`: Graphical interface.
  - `SummaryDisplay`: Command-line summary.
- `--agent1` & `--agent2`: Choose agents for players:
  - `KeyboardAgent`, `ReflexAgent`, `MinmaxAgent`, `AlphaBetaAgent`, `ExpectimaxAgent`, `QLearningAgent`, `MonteCarloAgent`.
- `--depth`: Max search depth for AI agents (default: 2).
- `--sleep_between_actions`: Whether to pause between actions (default: `False`).
- `--num_of_games`: Number of games to run (default: 1).
- `--evaluation_function1` & `--evaluation_function2`: Evaluation functions (default: `Hard`).

## Running Analysis

To perform an analysis on game results:

```bash
python3 analysis.py
```

## Agents

- **KeyboardAgent**: A human-controlled player.
- **ReflexAgent**: Simple AI making decisions based on the current state.
- **MinmaxAgent**: Uses the Minimax algorithm.
- **AlphaBetaAgent**: Optimized Minimax with Alpha-Beta pruning.
- **ExpectimaxAgent**: Uses the Expectimax algorithm.
- **QLearningAgent**: A reinforcement learning agent.
- **MonteCarloAgent**: Uses the Monte Carlo method.

