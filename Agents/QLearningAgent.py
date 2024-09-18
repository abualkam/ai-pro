from Agents.Agent import Agent
import abc
import random
import numpy as np


class QLearningAgent(Agent):
    def __init__(self, player, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=1, min_epsilon=0.01):
        super().__init__(player)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.Q = {}  # Q-table: {state: {action: Q-value}}


    def get_action(self, game_state):
        # Convert the game board to a tuple to use as a state key
        state = self._get_state_key(game_state)
        legal_actions = game_state.get_legal_actions(1)  # Assuming '1' is the agent's turn

        # Exploration vs. Exploitation
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(legal_actions)  # Explore: random action
        else:
            # Exploit: choose action with highest Q-value
            if state not in self.Q:
                self.Q[state] = {action: 0 for action in legal_actions}
            return max(self.Q[state], key=self.Q[state].get)

    def update(self, game_state, action, reward, next_game_state):
        # Update Q-values using the Q-learning formula
        state = self._get_state_key(game_state)
        next_state = self._get_state_key(next_game_state)
        if state not in self.Q:
            self.Q[state] = {a: 0 for a in game_state.get_legal_actions(self.player)}
        if next_state not in self.Q:
            self.Q[next_state] = {a: 0 for a in next_game_state.get_legal_actions(self.player)}

        if action not in self.Q[state]:
            self.Q[state][action] = 0
        # Q-learning update rule
        best_next_action = max(self.Q[next_state], key=self.Q[next_state].get)

        self.Q[state][action] = (1 - self.alpha) * self.Q[state][action] + self.alpha * (
                reward + self.gamma * self.Q[next_state][best_next_action]
        )

        # Decay the exploration rate
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def _get_state_key(self, game_state):
        # Converts the game board into a tuple representation
        return tuple(map(tuple, game_state.board))
