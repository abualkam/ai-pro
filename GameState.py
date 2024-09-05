import numpy as np
import copy

DEFAULT_COLUMNS = 7
DEFAULT_ROWS = 6
DEFAULT_BOARD_SIZE = 6


class GameState:
    def __init__(self, rows=DEFAULT_ROWS, columns=DEFAULT_COLUMNS, board=None, done=False, last_added = None):
        if board is None:
            board = np.zeros((rows, columns))
        self.__board = board
        self.__done = done
        self.__rows = rows
        self.__cols = columns
        if last_added is None:
            last_added = [rows] * columns
        self.__last_added = last_added
        self.__winner = 0
        self.__winner_cords = []


    @property
    def winner_coords(self):
        return self.__winner_cords

    @property
    def winner(self):
        return self.__winner

    @property
    def is_win(self):
        return self.__winner != 0

    @property
    def done(self):
        return self.__done or self._is_full

    @property
    def _is_full(self):
        return sum(self.__last_added) == 0

    @property
    def board(self):
        return self.__board

    def get_legal_actions(self, agent_index):
        return [col for col in range(len(self.__last_added)) if self.__last_added[col] > 0]

    def move(self, col, turn):
        if col is None:
            print(1)
        row = self.__last_added[col] - 1
        # TODO: check invalid human case
        self.__board[row][col] = turn
        if self.check_win((row, col), turn):
            self.__done = True
            self.__winner = turn
            return row, col
        if self._is_full:
            self.__done = True
            return row, col
        self.__last_added[col] -= 1
        return row, col

    def generate_successor(self, col, turn):
        new_board = copy.deepcopy(self.__board)
        last_added = copy.deepcopy(self.__last_added)

        successor = GameState(last_added= last_added, board= new_board,
                              rows=self.__rows, columns=self.__cols,done=self.__done)
        successor.move(col, turn)
        return successor

    def check_win(self, cor, player):
        #0,0 1,1 2,2, 3,3
        """
        this function checks checks if there are four squares that have the same disc
        :return: True if there are four squares that have the same disc, False if there aren't
        """
        (row, col) = cor
        directions = [(1, 0), (1, 1), (0, 1), (1, -1)]
        n_rows = self.__board.shape[0]
        n_cols = self.__board.shape[1]
        for ind1, ind2 in directions:
            count = 1
            i ,j= row + ind1, col + ind2
            coords = [(row,col)]
            while 0 <= i < n_rows and 0 <= j < n_cols and self.__board[i][j] == player:
                count += 1
                coords.append((i,j))
                i += ind1
                j += ind2

            i, j = row - ind1, col - ind2
            while 0 <= i < n_rows and 0 <= j < n_cols and self.__board[i][j] == player:
                count += 1
                coords.append((i,j))
                i -= ind1
                j -= ind2

            if count >=4 :
                self.__winner_cords = coords
                return True
        return False

    def valid_coordinate(self, cor):
        (row, col) = cor
        if (0 <= col <= self.__board.shape[1] - 1) and (0 <= row <= self.__board.shape[0] - 1):
            return True

        return False
