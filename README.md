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
python3 main.py --agent1=MonteCarloAgent --agent2=AlphaBetaAgent 
            --evaluation_function1=Easy --evaluation_function2=Easy --display=SummaryDisplay --num_of_games=10

##Game Options
* --random_seed: The seed for the random state (default: a random integer between 0 and 100).
* --display: The game UI to use. Choices are:
  * GUI: Graphical interface (default).
  * SummaryDisplay: Console-based display.
* --agent1: The first player agent. Choices are:
  * KeyboardAgent: Human player using keyboard input (default).
  * ReflexAgent: A simple AI agent.
  * MinmaxAgent: AI agent using the Minimax algorithm.
  * AlphaBetaAgent: AI agent using Alpha-Beta pruning.
  * ExpectimaxAgent: AI agent using the Expectimax algorithm.
* --agent2: The second player agent (same choices as --agent1).
* --depth: The maximum depth for AI search in the game tree (default: 2).
* --sleep_between_actions: Boolean flag indicating whether to sleep between actions (default: False).
* --num_of_games: The number of games to run (default: 1).
* --evaluation_function1: The evaluation function for the AI agent. Default is better.
* --evaluation_function2: The evaluation function for the AI agent. Default is better.


##Agents

* KeyboardAgent: A human player controlled via keyboard.
* ReflexAgent: A simple AI agent that makes decisions based on the current state.
* MinmaxAgent: An AI agent that uses the Minimax algorithm for decision-making.
* AlphaBetaAgent: An AI agent that optimizes Minimax with Alpha-Beta pruning.
* ExpectimaxAgent: An AI agent that uses the Expectimax algorithm for decision-making.