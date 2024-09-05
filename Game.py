import time


class Game(object):
    def __init__(self, agent=None, opponent_agent=None, display=None, sleep_between_actions=False):
        super(Game, self).__init__()
        self.sleep_between_actions = sleep_between_actions
        self.agent = agent
        self.display = display
        self.opponent_agent = opponent_agent
        self._state = None
        self._should_quit = False

    def run(self, initial_state):
        self._should_quit = False
        self._state = initial_state
        self.display.initialize(initial_state)
        return self._game_loop()

    def quit(self):
        self._should_quit = True
        self.agent.stop_running()
        self.opponent_agent.stop_running()

    def _game_loop(self):
        turn = 0
        while not self._state.done and not self._should_quit:

            if self.sleep_between_actions:
                time.sleep(1)
            if turn % 2 == 0:
                # print(self._state.board)
                action = self.agent.get_action(self._state)
                #self.agent.update()
                # print(self._state.board)
                cor1 = self._state.move(action, turn % 2 + 1)
                self.display.update_state(self._state, cor1, turn % 2 + 1)
            else:
                opponent_action = self.opponent_agent.get_action(self._state)
                cor2 = self._state.move(opponent_action, turn % 2 + 1)
                self.display.update_state(self._state, cor2, turn % 2 + 1)
            turn += 1

