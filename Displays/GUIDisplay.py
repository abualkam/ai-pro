import tkinter as tk
import tkinter.messagebox
import weakref
from abc import ABC
from tkinter import messagebox

from Displays.Display import Display


class Board:
    BALLS = {1: 'red', 2: 'yellow'}
    ROWS = 6
    COLUMNS = 7
    CIRCLE_DIAMETER = 80
    PADDING = 10

    def __init__(self, master):
        super().__init__()
        master.title("Four in a Row")
        self.__play_again = False
        # self.__game = game
        self._mouse_click_observers = []

        # Canvas size based on number of rows and columns
        canvas_width = self.COLUMNS * self.CIRCLE_DIAMETER + (self.COLUMNS + 1) * self.PADDING
        canvas_height = self.ROWS * self.CIRCLE_DIAMETER + (self.ROWS + 1) * self.PADDING
        self.__master = master
        # Create the canvas
        self.__canvas = tk.Canvas(master, width=canvas_width, height=canvas_height, bg='darkblue')
        self.__master.bind_all("<Button-1>", self._left_click_listener)
        self.__canvas.pack()

    def reset(self):
        self.__master.unbind_all("<Button-1>")
        self.__canvas.destroy()
        canvas_width = self.COLUMNS * self.CIRCLE_DIAMETER + (self.COLUMNS + 1) * self.PADDING
        canvas_height = self.ROWS * self.CIRCLE_DIAMETER + (self.ROWS + 1) * self.PADDING
        self.__canvas = tk.Canvas(self.__master, width=canvas_width, height=canvas_height, bg='darkblue')
        self.__canvas.pack()
        self.__master.bind_all("<Button-1>", self._left_click_listener)
        self.draw_board()

    def draw_board(self):
        """Draws the board with circles for the Connect Four game."""
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                x1 = col * self.CIRCLE_DIAMETER + (col + 1) * self.PADDING
                y1 = row * self.CIRCLE_DIAMETER + (row + 1) * self.PADDING
                x2 = x1 + self.CIRCLE_DIAMETER
                y2 = y1 + self.CIRCLE_DIAMETER
                # Draw a circle
                self.__canvas.create_oval(x1, y1, x2, y2, fill='white', outline='blue', width=5)

    def draw_ball(self, player, cor):
        """Draws a ball on the board based on the coordinates."""
        row, col = cor
        if player in self.BALLS:
            x1 = col * self.CIRCLE_DIAMETER + (col + 1) * self.PADDING
            y1 = row * self.CIRCLE_DIAMETER + (row + 1) * self.PADDING
            x2 = x1 + self.CIRCLE_DIAMETER
            y2 = y1 + self.CIRCLE_DIAMETER
            self.__canvas.create_oval(x1, y1, x2, y2, fill=self.BALLS[player], outline='blue', width=5)

    def specify_winner_balls(self, cor):
        """Highlights the balls that form the winning line."""
        # cor = self.__game.winner_coordinates()
        for row, col in cor:
            # row, col = cor[0][0] + i * cor[1][0], cor[0][1] + i * cor[1][1]
            x1 = col * self.CIRCLE_DIAMETER + (col + 1) * self.PADDING
            y1 = row * self.CIRCLE_DIAMETER + (row + 1) * self.PADDING
            x2 = x1 + self.CIRCLE_DIAMETER
            y2 = y1 + self.CIRCLE_DIAMETER
            self.__canvas.create_oval(x1, y1, x2, y2, outline='gold', width=5)

    def _left_click_listener(self, event):
        """Handle mouse left-click events and notify observers."""

        col = min(max(0, event.x - self.PADDING) // (self.CIRCLE_DIAMETER + self.PADDING), self.COLUMNS - 1)
        for observable in self._mouse_click_observers:
            observable()(col)

    def subscribe_to_mouse_click(self, observable):
        """Allow other parts of the program to subscribe to mouse click events."""
        # Store a weak reference to the observable to avoid strong reference issues
        self._mouse_click_observers.append(weakref.WeakMethod(observable))


class FourInARow(tk.Tk, Display):
    r"""
    Gabriele Cirulli's 2048 puzzle game;

    Python3-Tkinter port by Raphaël Seban;
    """

    def __init__(self):
        super(FourInARow, self).__init__()
        self.game_state = None
        self._board = Board(self)
        self.title("Four In A Row")
        self.resizable(width=False, height=False)
        self._board.draw_board()

    def subscribe_to_mouse_click(self, observable):
        """Allow other parts of the program to subscribe to mouse click events."""
        # Store a weak reference to the observable to avoid strong reference issues
        self._board.subscribe_to_mouse_click(observable)

    def initialize(self, initial_game_state):
        r"""
        widget's main inits;
        """

        self.withdraw()

        self.listen = True

        self.deiconify()
        self.game_state = initial_game_state
        self._board.reset()

    def quit_app(self, **kw):
        r"""
        quit app dialog;
        """
        if tkinter.messagebox.askokcancel("Question", "Quit game?", parent=self):
            # self._quit_game_callback()
            self.destroy()

    def update_state(self, state, cor, turn):
        # row,col = state.move(1, action)
        self._board.draw_ball(turn, (cor[0], cor[1]))
        if state.done and state.is_win:
            winner_coords = state.winner_coords
            self._board.specify_winner_balls(winner_coords)
        self.mainloop_iteration()

    def mainloop_iteration(self):
        self.update_idletasks()
        self.update()

    def play_again(self):
        if messagebox.askquestion('Game over', 'Do you want to play again?') == 'yes':
            return True
        return False
        #     self.new_game()