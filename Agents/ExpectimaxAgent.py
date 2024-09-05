from Agents.MultiSearchAgent import MultiAgentSearchAgent


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """
    def helper(self, game_state, depth,turn=0):
        legal_moves = game_state.get_legal_actions(turn % 2)
        if not legal_moves or depth == 0 :
            return self.evaluation_function(game_state, self.player) , None

        if turn % 2 == 0:  # Maximizing player
            max_score = -float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(action, self.player)
                score, _ = self.helper(successor, depth - 1, turn + 1)
                if score >= max_score:
                    max_score = score
                    best_action = action
            return max_score, best_action
        else:
            total_score = 0
            probability = 1 / len(legal_moves)
            for action in legal_moves:
                successor = game_state.generate_successor(action, self.opponent_player)
                score, _ = self.helper(successor, depth -1, turn + 1)
                total_score += probability * score
            return total_score, None

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        action =  self.helper(game_state, self.depth*2)[1]
        return action
