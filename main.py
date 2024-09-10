import argparse
import random

import numpy
import os

import Heuristics
from Displays.SummaryDisplay import SummaryDisplay
from Displays.GUIDisplay import FourInARow
from Agents.AlphaBetaAgent import  AlphaBetaAgent
from Agents.KeyboardAgent import  KeyboardAgent
from Agents.ExpectimaxAgent import ExpectimaxAgent
from Agents.MinmaxAgent import MinmaxAgent
from Agents.ReflexAgent import ReflexAgent
from Agents.QLearningAgent import QLearningAgent
from Agents.MonteCarloAgent import MonteCarloAgent
from  GameRunner import GameRunner
from GameState import GameState


def play_game(agent, opponent_agent=None):
    """Function to play a single game."""
    game_state = GameState()  # Start a new game
    done = False

    while not done:
        # Agent's turn
        action = agent.get_action(game_state)  # Get the action from the Q-learning agent
        row, col = game_state.move(action, 1)  # Agent is player '1'

        # Check if the game is over after agent's move
        if game_state.done:
            if game_state.is_win:
                reward = 1  # Win for the agent
            else:
                reward = 0  # Draw
            agent.update(game_state, action, reward, game_state)  # Update Q-table with the final state
            break

        # Opponent's turn
        if opponent_agent:
            opponent_action = opponent_agent.get_action(game_state)
        else:
            opponent_action = random.choice(game_state.get_legal_actions(2))  # Random move for the opponent

        row, col = game_state.move(opponent_action, 2)  # Opponent is player '2'

        # Check if the game is over after opponent's move
        if game_state.done:
            if game_state.is_win:
                reward = -1  # Loss for the agent
            else:
                reward = 0  # Draw
            agent.update(game_state, action, reward, game_state)  # Update Q-table with the final state
            break

        # Update Q-table for non-terminal state if training
        reward = -1  # Small negative reward to encourage quicker wins
        next_state = game_state.generate_successor(action, 1)
        agent.update(game_state, action, reward, next_state)

        # Continue to the next state
        game_state = next_state

    return reward


def train_agent(agent, episodes=5000):
    opponents = [
        (episodes,"Random", ReflexAgent(player=2)),
        (episodes,"EasyMinmax", AlphaBetaAgent(depth=2, evaluation_function=Heuristics.easy_evaluation_function, player=2)),
        (episodes,"MediumMinmax", AlphaBetaAgent(depth=2, evaluation_function=Heuristics.medium_evaluation_function, player=2)),
        (episodes,"HardMinmax", AlphaBetaAgent(depth=2, evaluation_function=Heuristics.hard_evaluation_function, player=2)),
    ]

    for episodes, opponent_name, opponent in opponents:
        print(f"Training against {opponent_name} agent.")
        for episode in range(episodes):
            play_game(agent, opponent_agent=opponent)
            if episode % 1000 == 0:
                print(f"Episode {episode} against {opponent_name}, Number of states: {len(agent.Q)}")

                # if agent.epsilon == agent.min_epsilon:
                #     agent.epsilon = 1
                #     break
                #
        # print(f"Finished training
        # against {opponent_name} agent.")

    print("Training against all types complete!")

def evaluate_agent(agent, games=1000):
    """Function to evaluate the trained agent against a random player."""
    wins = 0
    losses = 0
    draws = 0

    for _ in range(games):
        result = play_game(agent)
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            draws += 1

    print(f"Evaluation: Wins: {wins}, Losses: {losses}, Draws: {draws}")



def create_display(display_name):
    if display_name == "GUI":
        return FourInARow()
    elif display_name == "SummaryDisplay":
        return SummaryDisplay()
    raise Exception("Invalid summary display type.")

def create_agent(agent_name,player , evaluation_function, depth, display):
    if agent_name == "MinmaxAgent":
        return MinmaxAgent(depth=depth, evaluation_function=evaluation_function, player=player)
    elif agent_name == "ExpectimaxAgent":
        return ExpectimaxAgent(depth=depth, evaluation_function=evaluation_function, player=player)
    elif agent_name == "AlphaBetaAgent":
        return AlphaBetaAgent(depth=depth, evaluation_function=evaluation_function, player=player)
    elif agent_name == "KeyboardAgent":
        return KeyboardAgent(display)
    elif agent_name == "QLearningAgent":
        model = QLearningAgent(player=player)
        train_agent(model)
        # model.t
        return model
    elif agent_name == "MonteCarloAgent":
        return MonteCarloAgent()
    raise Exception("Invalid agent name.")

def create_evaluation_function(difficulty):
    if difficulty == "Easy":
        return Heuristics.easy_evaluation_function
    elif difficulty == "Medium":
        return Heuristics.medium_evaluation_function
    elif difficulty == "Hard":
        return Heuristics.hard_evaluation_function

    raise Exception("Invalid heuristic difficulty.")
def main():
    parser = argparse.ArgumentParser(description='2048 game.')
    parser.add_argument('--random_seed', help='The seed for the random state.', default=numpy.random.randint(100), type=int)
    displays = ['GUI', 'SummaryDisplay']
    agents = ['KeyboardAgent', 'ReflexAgent', 'MinmaxAgent', 'AlphaBetaAgent', 'ExpectimaxAgent', 'QLearningAgent', 'MonteCarloAgent']
    parser.add_argument('--display', choices=displays, help='The game ui.', default="GUI", type=str)
    parser.add_argument('--agent1', choices=agents, help='The agent.', default='AlphaBetaAgent', type=str)
    parser.add_argument('--agent2', choices=agents, help='The agent.', default='AlphaBetaAgent'
                                                                               , type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=2, type=int)
    parser.add_argument('--sleep_between_actions', help='Should sleep between actions.', default=False, type=bool)
    parser.add_argument('--num_of_games', help='The number of games to run.', default=1, type=int)
    parser.add_argument('--evaluation_function1', help='The evaluation function for ai agent.',
                        default='Hard', type=str)
    parser.add_argument('--evaluation_function2', help='The evaluation function for ai agent.',
                        default='Hard', type=str)

    args = parser.parse_args()
    numpy.random.seed(args.random_seed)
    display = create_display(args.display)
    evaluation_function1 = create_evaluation_function(args.evaluation_function1)
    evaluation_function2 = create_evaluation_function(args.evaluation_function2)
    agent1 = create_agent(args.agent1,1,evaluation_function1,args.depth,display)
    agent2 = create_agent(args.agent2,2,evaluation_function2,args.depth, display)

    # if args.agent1 == "QLearningAgent":
    #     train_agent(agent1)
    game_runner = GameRunner(display=display, agent1=agent1,agent2=agent2,
                             sleep_between_actions=args.sleep_between_actions)
    for i in range(args.num_of_games):
        print(i)
        score = game_runner.new_game(initial_state=None)

    print(display.print_stats())
    # if display is not None:
    #     display.print_stats()
    # return scores

if __name__ == '__main__':
    main()
    input("Press Enter to continue...")
