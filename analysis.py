import threading
import numpy as np
import os
import time
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
import matplotlib.pyplot as plt


def create_evaluation_function(difficulty):
    if difficulty == "Easy":
        return Heuristics.easy_evaluation_function
    elif difficulty == "Medium":
        return Heuristics.medium_evaluation_function
    elif difficulty == "Hard":
        return Heuristics.hard_evaluation_function
    
def create_agent(agent_name,player , depth, display):
    
    if "Easy" in agent_name:
        evaluation_function = create_evaluation_function("Easy")
        agent_name = agent_name.replace("Easy","")
    elif "Medium" in agent_name:
        evaluation_function = create_evaluation_function("Medium")
        agent_name = agent_name.replace("Medium","")
    elif  "Hard" in agent_name:
        evaluation_function = create_evaluation_function("Hard")
        agent_name = agent_name.replace("Hard","")
        
    if agent_name == "MinmaxAgent":
        return MinmaxAgent(depth=depth, evaluation_function=evaluation_function, player=player)
    elif agent_name == "ExpectimaxAgent":
        return ExpectimaxAgent(depth=depth, evaluation_function=evaluation_function, player=player)
    elif agent_name == "AlphaBetaAgent":

        return AlphaBetaAgent(depth=depth, evaluation_function=evaluation_function, player=player)
    elif agent_name == "ReflexAgent":
        return ReflexAgent(player=player)
    # elif agent_name == "QLearningAgent":
    #     model = QLearningAgent(player=player)
    #     train_agent(model)
    #     return model
    elif agent_name == "MonteCarloAgent":
        return MonteCarloAgent(player)
    
    raise Exception("Invalid agent name." +agent_name)


mutex = threading.Lock()

def run_n_games(index_i,index_j,num,ag1,ag2,dis):
    for q in range(num):
            # Initialize game
            print(f'game number {q}')
            game = GameRunner(display=dis,agent1=ag1, agent2=ag2)
            start_time = time.time()
            # Play game and get result
            game.new_game(initial_state=None) 
            
    with mutex:
        
        win_matrix[index_i, index_j] = display.winner.count(1) / num_games
        draw_matrix[index_i, index_j] = display.winner.count(0) / num_games
        lose_matrix[index_i, index_j] = display.winner.count(2) / num_games

        print(display.winner)
        print(display.num_steps)
        print(display.game_durations)
        num_moves[index_i, index_j] = sum(display.num_steps) / num_games
        times[index_i, index_j] = sum(display.game_durations) / num_games

display = SummaryDisplay()
agent_names = ['EasyAlphaBetaAgent','MediumAlphaBetaAgent','HardAlphaBetaAgent', 'EasyExpectimaxAgent','MediumExpectimaxAgent','HardExpectimaxAgent','EasyMinmaxAgent','MediumMinmaxAgent', 'HardMinmaxAgent', 'MonteCarloAgent', 'ReflexAgent']
# Initialize metrics storage
n_agents = len(agent_names)
win_matrix = np.zeros((n_agents, n_agents))
draw_matrix = np.zeros((n_agents, n_agents))
lose_matrix = np.zeros((n_agents, n_agents))
num_moves = np.zeros((n_agents,n_agents))  # To store average number of moves for each agent vs another agent
times = np.zeros((n_agents, n_agents))      # To store average time taken for each agent vs another agent

num_games = 100
display = SummaryDisplay()
# Run games between each pair of agents
threads = []
for i in range(len(agent_names)):
    
    for j in range(len(agent_names)):
        display = SummaryDisplay()
        agent1 = create_agent(agent_names[i], 1,2,display )
        agents_arr = [agent_names[i],agent_names[j]]
        print(f'agent1:{agent_names[i]} vs agent2:{agent_names[j]}')
        agent2 = create_agent(agent_names[j], 2,2,display)

        for q in range(num_games):
            # Initialize game
            print(f'game number {q}')
            game = GameRunner(display=display,agent1=agent1, agent2=agent2)
            start_time = time.time()
            # Play game and get result
            game.new_game(initial_state=None)

        # Store win rates, number of moves, and time
        win_matrix[i, j] = display.winner.count(1) / num_games
        draw_matrix[i, j] = display.winner.count(0) / num_games
        lose_matrix[i, j] = display.winner.count(2) / num_games

        print(display.winner)
        print(display.num_steps)
        print(display.game_durations)
        num_moves[i, j] = sum(display.num_steps) / num_games
        times[i, j] = sum(display.game_durations) / num_games

    # for thread in threads:
    #     thread.join() 

# Plot results
def plot_metrics(matrix, title, labels):
    fig, ax = plt.subplots(figsize=(10, 8))  # Increased figure size
    cax = ax.matshow(matrix, cmap='coolwarm')
    plt.title(title)
    fig.colorbar(cax)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))

    ax.set_xticklabels(labels, rotation=45, ha='left')  # Rotated labels for better visibility
    ax.set_yticklabels(labels)

    # Annotate each cell with the value
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f'{matrix[i, j]:.2f}', va='center', ha='center')

    plt.tight_layout()
    plt.show()



plot_metrics(win_matrix, 'Win Rate Heatmap', agent_names)

# Plot Win Rates
plot_metrics(draw_matrix, 'Draw Rate Heatmap', agent_names)

# Plot Win Rates
plot_metrics(lose_matrix, 'Lose Rate Heatmap', agent_names)

# Plot Number of Moves
plot_metrics(num_moves, 'Average Number of Moves Heatmap', agent_names)

# Plot Time Taken
plot_metrics(times, 'Average Time Taken Heatmap (seconds)', agent_names)

