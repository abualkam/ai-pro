from tkinter import messagebox

from Game import Game
from GameState import GameState

class GameRunner(object):
    def __init__(self, display=None, agent1=None,agent2=None,
                 sleep_between_actions=False):
        super(GameRunner, self).__init__()
        self.sleep_between_actions = sleep_between_actions
        self.human_agent = agent1 is None
        self.display = display
        self._agent1 = agent1
        self._agent2 = agent2
        self.current_game = None

    def new_game(self, initial_state=None, *args, **kw):
        self.quit_game()
        if initial_state is None:
            initial_state = GameState()
        game = Game(self._agent1, self._agent2, self.display, sleep_between_actions=self.sleep_between_actions)
        self.current_game = game
        game.run(initial_state)
        if self.display.play_again():
            self.new_game()
        #     self.new_game()

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()
