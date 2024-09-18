import abc

from Agents.Agent import Agent


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (Game.py)
    is another abstract class.
    """

    def __init__(self, player, evaluation_function, depth=2):
        super().__init__(player)

        self.evaluation_function = evaluation_function
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return
