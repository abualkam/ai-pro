import random
from collections import defaultdict
from Agents.Agent import Agent
import copy


class MonteCarloAgent(Agent):
    def __init__(self, player, num_simulations=100, discount_factor=1.0, exploration_factor=1.0):
        super().__init__(player)
        self.player = player
        self.num_simulations = num_simulations
        self.discount_factor = discount_factor
        self.exploration_factor = exploration_factor
        self.returns = defaultdict(list)
        self.value_function = defaultdict(float)
        self.visit_counts = defaultdict(int)  # Count visits to each state

    def get_action(self, game_state):
        """
        Get the best action for the agent's player.
        """
        legal_actions = game_state.get_legal_actions(self.player)
        best_action = None
        best_score = float('-inf')

        # Run simulations for each legal action
        for action in legal_actions:
            avg_return = self.simulate_action(game_state, action)
            if avg_return > best_score:
                best_score = avg_return
                best_action = action

        return best_action

    def simulate_action(self, game_state, action):
        """
        Run multiple simulations for a given action and return the average reward.
        Simulates the action for self.player.
        """
        total_return = 0
        for _ in range(self.num_simulations):
            total_return += self.simulate_episode(game_state, action)

        avg_return = total_return / self.num_simulations
        return avg_return

    def simulate_episode(self, initial_state, initial_action):
        """
        Simulate a full episode starting from the given initial action for self.player.
        """
        state = copy.deepcopy(initial_state)
        state.move(initial_action, self.player)  # The agent makes the initial move

        episode = [(state, 0)]  # Store the state and reward
        current_player = 3 - self.player  # Switch to the opponent

        # Play the rest of the episode
        while not state.done:
            legal_actions = state.get_legal_actions(current_player)
            action = self.select_move(state, legal_actions, current_player)
            state.move(action, current_player)
            reward = self.get_reward(state, current_player)
            episode.append((copy.deepcopy(state), reward))
            current_player = 3 - current_player  # Alternate players

        # Update the value function for the episode
        G = 0
        for t in reversed(range(len(episode))):
            state_t, reward_t = episode[t]
            G = self.discount_factor * G + reward_t
            state_key = self.state_to_key(state_t)
            if state_key not in [self.state_to_key(s) for s, _ in episode[:t]]:
                self.visit_counts[state_key] += 1
                alpha = 1.0 / self.visit_counts[state_key]
                self.value_function[state_key] += alpha * (G - self.value_function[state_key])

        return G

    def select_move(self, state, legal_actions, player):
        """
        Select a move for the given player, incorporating a heuristic that prefers central columns.
        """
        if random.random() < self.exploration_factor:
            return random.choice(legal_actions)
        else:
            center = state._cols // 2
            scores = {}

            for action in legal_actions:
                column_distance = abs(center - action)
                scores[action] = -column_distance  # More negative distance is better (closer to center)

            best_action = max(scores, key=scores.get)
            return best_action

    def get_reward(self, state, player):
        """
        Calculate reward based on the state and the player.
        """
        if state.winner == self.player:
            return 1
        elif state.winner == 3 - self.player:
            return -1
        else:
            return 0

    def state_to_key(self, state):
        """
        Convert the game state into a hashable key.
        """
        return tuple(map(tuple, state.board))

    def stop_running(self):
        pass

    def update(self, game_state, action, reward, next_game_state):
        pass
