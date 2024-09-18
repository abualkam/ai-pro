import abc


class Agent:
    def __init__(self, player):
        self.player = player
        self.opponent_player = 1 if player == 2 else 2
    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def stop_running(self):
        pass

    def update(self, game_state, action, reward, next_game_state):
        pass