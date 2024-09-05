from Agents.MultiSearchAgent import MultiAgentSearchAgent


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def helper(self, game_state, depth, alpha=-float('inf'), beta=float('inf'), turn=0):
        legal_moves = game_state.get_legal_actions(turn % 2)
        if game_state.done or depth == 0:
            return self.evaluation_function(game_state, self.player), None

        if turn % 2 == 0:
            max_score = -float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(action, self.player)
                score, _ = self.helper(successor, depth - 1, alpha, beta, turn + 1)
                if score > max_score:
                    max_score = score
                    best_action = action
                alpha = max(alpha, score)
                if beta <= alpha:
                    break

            return max_score, best_action
        else:
            min_score = float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(action, self.opponent_player)
                score, _ = self.helper(successor, depth -1, alpha, beta, turn + 1)
                if score < min_score:
                    min_score = score
                    best_action = action
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_action

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """*** YOUR CODE HERE ***"""
        action =  self.helper(game_state, self.depth*2)[1]
        return action
