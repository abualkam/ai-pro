from abc import ABC, abstractmethod

class Display(ABC):
    @abstractmethod
    def initialize(self, initial_state):
        pass

    @abstractmethod
    def update_state(self, new_state, action, opponent_action):
        pass

    def mainloop_iteration(self):
        pass

    def print_stats(self):
        pass

    def play_again(self):
        pass