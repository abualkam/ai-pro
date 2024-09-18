from Agents.Agent import Agent

class KeyboardAgent(Agent):
    """
    An agent controlled by the keyboard.
    """
    LEFT_KEY = 'a'
    RIGHT_KEY = 'd'
    UP_KEY = 'w'
    DOWN_KEY = 's'

    def __init__(self, player,tk_window):
        super().__init__(player)
        self.keys = []
        tk_window.subscribe_to_mouse_click(self.listener)
        self.tk_window = tk_window
        self._should_stop = False
        self._move = None
    def get_action(self, state):
        self._should_stop = False
        move = self._move
        while move is None and not self._should_stop:
            self.tk_window.mainloop_iteration()
            move = self._move
        self._move = None
        return move

    def stop_running(self):
        self._should_stop = True


    def listener(self, tk_event=None, *args, **kw):

        self._move = tk_event