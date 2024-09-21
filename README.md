# Four in a Row Game

This is a Python implementation of the classic "Four in a Row" (also known as "Connect Four") game, featuring a graphical user interface (GUI) and support for different types of AI agents. You can play against another human or one of several AI agents using different algorithms.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Game Options](#game-options)
- [Agents](#agents)
- [Examples](#examples)

## Installation

To run the game, you'll need Python 3.x.

Install the required dependencies using the `requirements.txt` file:

```
pip install -r requirements.txt
```
## Usage
python3 main.py --agent1 <Agent1> --agent2 <Agent2> --display <DisplayType> [OPTIONS]

## Game Options
* --random_seed: Set the random state seed (default: a random integer).
* --display: The game UI type. Available options:
** GUI (Graphical interface)
** SummaryDisplay (Command-line summary)
* --agent1: Player 1 agent. Options include:
** KeyboardAgent, ReflexAgent, MinmaxAgent, AlphaBetaAgent, ExpectimaxAgent, QLearningAgent, MonteCarloAgent
* --agent2: Player 2 agent (same choices as --agent1).
* --depth: Maximum search depth in the game tree (default: 2).
* --sleep_between_actions: Boolean flag to control pauses between actions (default: False).
* --num_of_games: Number of games to simulate (default: 1).
* --evaluation_function1: Evaluation function for Player 1 (default: Hard).
* --evaluation_function2: Evaluation function for Player 2 (default: Hard).

## Running Analysis
To perform an analysis of the game results, run the following command:

python3 analysis.py

## Agents

* KeyboardAgent: A human player controlled via keyboard.
* ReflexAgent: A simple AI agent that makes decisions based on the current state.
* MinmaxAgent: An AI agent that uses the Minimax algorithm for decision-making.
* AlphaBetaAgent: An AI agent that optimizes Minimax with Alpha-Beta pruning.
* ExpectimaxAgent: An AI agent that uses the Expectimax algorithm for decision-making.
