import time

import numpy as np

from Displays.Display import Display


class SummaryDisplay(Display):
    def __init__(self):
        super(SummaryDisplay, self).__init__()
        self.winner = []
        self.game_durations = []
        self.game_start_time = None
        self.num_steps= []
    def initialize(self, initial_state):
        self.game_start_time = time.time()

    def update_state(self, new_state, action, opponent_action):
        if new_state.done:
            game_end_time = time.time()
            game_duration = game_end_time - self.game_start_time
            # print("winner: %s\ngame_duration: %s" % (new_state.winner, game_duration))
            self.winner.append(new_state.winner)
            # self.highest_tile.append(new_state.board.max())
            self.game_durations.append(game_duration)
            b = new_state.board
            self.num_steps.append(np.count_nonzero(b))


    def print_stats(self):
        return self.winner, self.game_durations,self.num_steps