import math

import numpy as np


def evaluate_depth(board, player):
    """
    Evaluate the board based on the depth of pieces.
    Parameters:
    - board: 2D list representing the Connect Four board
    - player: int (1 for AI player, -1 for opponent)

    Returns:
    - int: The score based on depth
    """
    score = 0
    opponent_player = 1 if player == 2 else 2
    col_weights = [1, 2, 4, 8, 4, 2, 1]
    rows = board.shape[0]
    center_column = board.shape[1]//2
    for row in range(board.shape[0]):

        for col in range(board.shape[1]):
            if board[row, col] == player:
                # Deeper rows (closer to the bottom) are more valuable
                # Assign a higher score to lower rows
                score += row * col_weights[col]
            elif board[row, col] == opponent_player:
                # Penalize for opponent's pieces in the same way
                score -= row * col_weights[col]
    # for row in range(rows):
    #     if board[row][center_column] == player:
    #         score += 3  # Control of center column
    #     elif board[row][center_column] == -player:
    #         score -= 3  # Penalize for opponent's control
    return score


def evaluate_center_control(board, player):
    """
    Evaluate the board based on control of the center columns.

    Parameters:
    - board: 2D list representing the Connect Four board
    - player: int (1 for AI player, -1 for opponent)

    Returns:
    - int: The score based on center control
    """
    score = 0
    center_column = (board.shape[1]) // 2
    opponent_player = 1 if player == 2 else 2

    for row in range(board.shape[0]):
        if board[row, center_column] == player:
            score += 10  # Assign higher score for controlling the center column
        elif board[row, center_column] == opponent_player:
            score -= 10  # Penalize for opponent's control

    return score


# def evaluate_four_connected(game_state, player):
#     """
#     four connected -> inf
#     three connected with open end -> high score
#     two connected with two open ends -> medium score
#     one connected with mulltiple open spaces -> low score
#     :param game_state:
#     :param player:
#     :return:
#     """
#     pass


def evaluate_opponent_moves(game_state, player):
    """
    -1 * evaluate_four_connected(game_state, opponent_player)
    :param game_state:
    :param opponent_player:
    :return:
    """
    pass


def score_position(board, player):
    score = 0
    opponent = 1 if player == 2 else 2

    # Prioritize the center column
    center_column_index = board.shape[1] // 2
    center_column = [int(i) for i in list(board[:, center_column_index])]
    center_count = center_column.count(player)
    score += center_count * 10  # High weight for center column

    # Horizontal scoring
    for row in range(board.shape[0]):
        row_array = [i for i in list(board[row, :])]
        for col in range(board.shape[1] - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, player, opponent, center_column_index)

    # Vertical scoring
    for col in range(board.shape[1]):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(board.shape[0] - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, player, opponent, center_column_index)

    # Positive sloped diagonal scoring
    for row in range(board.shape[0] - 3):
        for col in range(board.shape[1] - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, player, opponent, center_column_index)

    # Negative sloped diagonal scoring
    for row in range(board.shape[0] - 3):
        for col in range(board.shape[1] - 3):
            window = [board[row + 3 - i][col + i] for i in range(4)]
            score += evaluate_window(window, player, opponent, center_column_index)

    return score


def evaluate_window(window, player, opponent, center_column_index):
    score = 0

    if window.count(player) == 4:
        score += 1000  # Maximize winning
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 100  # High score for potential winning move
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 10  # Score for potential 2 in a row

    # Boost score if window includes center column
    # for i, pos in enumerate(window):
    #     if pos == player and center_column_index - 1 <= i <= center_column_index + 1:
    #         score += 10  # Additional boost for center column involvement

    # Block opponent
    # if window.count(opponent) == 3 and window.count(0) == 1:
    #     score -= 80  # Strong negative score to prioritize blocking

    return score


def evaluate_four_connected(board, player):
    """
    four connected -> inf
    three connected with open end -> high score
    two connected with two open ends -> medium score
    one connected with mulltiple open spaces -> low score
    :param game_state:
    :param player:
    :return:
    """

    def check_sequences(board, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # vertical, horizontal, diagonal down-right, diagonal down-left
        counts = {2: 0, 3: 0, 4: 0}  # Counts for the given player

        def count_in_direction(row, col, d_row, d_col):
            count = 0
            r, c = row, col
            # Check in one direction
            while 0 <= r < board.shape[0] and 0 <= c < board.shape[1] and board[r, c] == player:
                count += 1
                r += d_row
                c += d_col

            r, c = row - d_row, col - d_col
            # Check in the opposite direction
            while 0 <= r < board.shape[0] and 0 <= c < board.shape[1] and board[r, c] == player:
                count += 1
                r -= d_row
                c -= d_col

            return count

        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col] == player:  # Only check spots occupied by the player
                    for d_row, d_col in directions:
                        sequence_length = count_in_direction(row, col, d_row, d_col)
                        for seq in [2, 3, 4]:
                            if sequence_length == seq:
                                counts[seq] += 1

        return counts

    score = check_sequences(board, player)
    # print(game_state.board)
    # print("------------------------")
    # print("######",score)
    # if score[4] != 0:
    #     # print("helllooooooo")
    #     return float("inf")
    return score[2] * 10 + score[3] * 100 + score[4] * 1000


def get_heuristic_score(board, player):
    return score_position(board, player)


def check_figure_7_trap(board, player):
    rows = len(board)
    cols = len(board[0])

    for r in range(2, rows):  # Start from row 2 to ensure we have space for diagonal
        for c in range(cols - 2):  # Start from column 0 to leave space for 3-piece horizontal
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player:
                # Check vertical alignment for the "7" figure
                if board[r-1][c+2] == player and board[r-2][c+2] == player:
                    # This matches the "figure 7 trap"
                    return True
    return False


def count_possible_fours(board, player):
    """
    Count the number of possible 4-in-a-row combinations for the given player.

    :param board: 2D list representing the Connect Four board.
    :param player: The player to evaluate ('R' for Red or 'Y' for Yellow).
    :return: Integer count of possible 4-in-a-rows for the player.
    """
    rows, cols = len(board), len(board[0])
    count = 0

    # Check horizontal combinations
    for r in range(rows):
        for c in range(cols - 3):  # Check only till the 4th last column
            if all(board[r][c + i] in (player, 0) for i in range(4)):
                count += 1

    # Check vertical combinations
    for c in range(cols):
        for r in range(rows - 3):  # Check only till the 4th last row
            if all(board[r + i][c] in (player, 0) for i in range(4)):
                count += 1

    # Check diagonal up-right combinations
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] in (player, 0) for i in range(4)):
                count += 1

    # Check diagonal down-right combinations
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] in (player, 0) for i in range(4)):
                count += 1

    return count


def heuristic(board, player):
    """
    Heuristic function to evaluate the board.

    :param board: 2D list representing the Connect Four board.
    :return: Integer heuristic value.
    """
    opponent = 1 if player == 2 else 2

    red_count = count_possible_fours(board, player)
    yellow_count = count_possible_fours(board, opponent)

    return red_count - yellow_count


def hard_evaluation_function(game_state, player):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current GameState and returns a number, where higher numbers are better.
    """
    opponent = 1 if player == 2 else 2

    depth = evaluate_depth(game_state.board, player)
    four_connected = score_position(game_state.board, player)
    opponent_four_connected = score_position(game_state.board, opponent)

    return depth + four_connected -  opponent_four_connected
def medium_evaluation_function(game_state, player):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current GameState and returns a number, where higher numbers are better.
    """
    opponent = 1 if player == 2 else 2

    # depth = evaluate_depth(game_state.board, player)
    four_connected = score_position(game_state.board, player)
    opponent_four_connected = score_position(game_state.board, opponent)

    return four_connected -  opponent_four_connected
def easy_evaluation_function(game_state, player):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current GameState and returns a number, where higher numbers are better.
    """
    opponent = 1 if player == 2 else 2

    # depth = evaluate_depth(game_state.board, player)
    four_connected = score_position(game_state.board, player)
    # opponent_four_connected = score_position(game_state.board, opponent)

    return four_connected



