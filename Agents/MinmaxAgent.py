import math

from Agents.MultiSearchAgent import MultiAgentSearchAgent


class MinmaxAgent(MultiAgentSearchAgent):
    def helper(self, game_state, depth, turn=0):
        legal_moves = game_state.get_legal_actions(turn % 2)
        if  game_state.done or depth == 0:
            return self.evaluation_function(game_state, self.player), None

        if turn % 2 == 0:
            max_score = -float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(action, self.player)
                score, _ = self.helper(successor, depth - 1, turn + 1)
                if score > max_score:
                    max_score = score
                    best_action = action
            return max_score, best_action
        else:
            min_score = float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(action, self.opponent_player)
                score, _ = self.helper(successor, depth - 1, turn + 1)
                if score < min_score:
                    min_score = score
                    best_action = action
            return min_score, best_action


    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        """*** YOUR CODE HERE ***"""
        action = self.helper(game_state, 2 *self.depth )[1]
        return action
