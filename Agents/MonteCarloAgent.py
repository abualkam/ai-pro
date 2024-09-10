import random
from collections import defaultdict
from Agents.Agent import Agent
import copy
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


class MonteCarloAgent(Agent):
    def __init__(self, num_simulations=100, discount_factor=1.0, exploration_factor=1.0):
        super().__init__()
        self.num_simulations = num_simulations
        self.discount_factor = discount_factor
        self.exploration_factor = exploration_factor
        self.returns = defaultdict(list)
        self.value_function = defaultdict(float)
        self.visit_counts = defaultdict(int)  # Count visits to each state

    def get_action(self, game_state):
        legal_actions = game_state.get_legal_actions(1)
        best_action = None
        best_score = float('-inf')

        # Run simulations in parallel
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda action: self.simulate_action(game_state, action), legal_actions))

        # Find the action with the highest average reward
        for action, avg_return in results:
            if avg_return > best_score:
                best_score = avg_return
                best_action = action

        return best_action

    def simulate_action(self, game_state, action):
        """
        Run multiple simulations for a given action and return the average reward.
        """
        total_return = 0
        for _ in range(self.num_simulations):
            total_return += self.simulate_episode(game_state, action)
        avg_return = total_return / self.num_simulations
        return action, avg_return

    def simulate_episode(self, initial_state, initial_action):
        state = copy.deepcopy(initial_state)
        state.move(initial_action, 1)

        episode = [(state, 0)]
        current_player = 2

        while not state.done:
            legal_actions = state.get_legal_actions(current_player)
            action = self.select_move(state, legal_actions, current_player)
            state.move(action, current_player)

            reward = self.get_reward(state, current_player)
            episode.append((copy.deepcopy(state), reward))
            current_player = 3 - current_player

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
        # Heuristic: Prefer moves that block opponent wins or create multiple threats
        if random.random() < self.exploration_factor:
            return random.choice(legal_actions)
        else:
            # Use a simple heuristic (e.g., prefer center column or prevent opponent's win)
            center = state._cols // 2
            if center in legal_actions:
                return center
            else:
                return random.choice(legal_actions)

    def get_reward(self, state, player):
        if state.winner == 1:
            return 1
        elif state.winner == 2:
            return -1
        else:
            return 0

    def state_to_key(self, state):
        return tuple(map(tuple, state.board))

    def stop_running(self):
        pass

    def update(self, game_state, action, reward, next_game_state):
        pass

# class MonteCarloAgent(Agent):
#     def __init__(self, num_simulations=100, discount_factor=1.0):
#         super().__init__()
#         self.num_simulations = num_simulations
#         self.discount_factor = discount_factor
#         self.returns = defaultdict(list)  # Dictionary to store returns for each state
#         self.value_function = defaultdict(float)  # State-value function V(s)
#
#     def get_action(self, game_state):
#         legal_actions = game_state.get_legal_actions(1)  # Assuming '1' is the Monte Carlo Agent's turn
#         best_action = None
#         best_score = float('-inf')
#
#         # Evaluate each legal action using Monte Carlo simulations
#         for action in legal_actions:
#             total_return = 0
#
#             # Simulate `num_simulations` games for this action
#             for _ in range(self.num_simulations):
#                 total_return += self.simulate_episode(game_state, action)
#
#             # Calculate the average return for this action
#             avg_return = total_return / self.num_simulations
#
#             # Select the action with the highest average return
#             if avg_return > best_score:
#                 best_score = avg_return
#                 best_action = action
#
#         return best_action
#
#     def simulate_episode(self, initial_state, initial_action):
#         """
#         Simulate a full episode starting with the given initial action.
#         Returns the cumulative discounted reward from the initial state.
#         """
#         state = copy.deepcopy(initial_state)
#         state.move(initial_action, 1)  # Monte Carlo Agent makes the initial move
#
#         episode = [(state, 0)]  # Stores the states and corresponding rewards
#         current_player = 2  # Start with the opponent's turn
#
#         # Continue the episode until the game ends
#         while not state.done:
#             legal_actions = state.get_legal_actions(current_player)
#             action = random.choice(legal_actions)
#             state.move(action, current_player)
#
#             reward = self.get_reward(state, current_player)
#             episode.append((copy.deepcopy(state), reward))
#             current_player = 3 - current_player  # Toggle between player 1 and player 2
#
#         # Calculate returns for each state in the episode
#         G = 0
#
#         for t in reversed(range(len(episode))):
#             state_t, reward_t = episode[t]
#             G = self.discount_factor * G + reward_t
#
#             # Only update if this is the first visit to the state in this episode
#             state_key = self.state_to_key(state_t)
#             if state_key not in [self.state_to_key(s) for s, _ in episode[:t]]:
#                 self.returns[state_key].append(G)
#                 self.value_function[state_key] = sum(self.returns[state_key]) / len(self.returns[state_key])
#
#         return G
#
#     def get_reward(self, state, player):
#         if state.winner == 1:
#             return 1  # Win for Monte Carlo Agent
#         elif state.winner == 2:
#             return -1  # Loss for Monte Carlo Agent
#         else:
#             return 0  # No winner yet or draw
#
#     def state_to_key(self, state):
#         return tuple(map(tuple, state.board))  # Convert board array to a hashable tuple
#
#     def stop_running(self):
#         pass
#
#     def update(self, game_state, action, reward, next_game_state):
#         # Monte Carlo does not require direct updates during the game, handled by simulate_episode
#         pass
