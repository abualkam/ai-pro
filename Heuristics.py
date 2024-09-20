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
    col_weights = [2, 4, 8, 16, 8, 4, 2]

    for row in range(board.shape[0]):

        for col in range(board.shape[1]):
            if board[row, col] == player:

                score += row * col_weights[col]
            elif board[row, col] == opponent_player:
                score -= row * col_weights[col]

    return score


def get_windows(board, window_size=4):
    """
    Generator that yields all horizontal, vertical, and diagonal windows of the specified size from the board.
    """
    # Horizontal windows
    for row in range(board.shape[0]):
        for col in range(board.shape[1] - window_size + 1):
            yield board[row, col:col + window_size]  # 4 horizontal cells

    # Vertical windows
    for col in range(board.shape[1]):
        for row in range(board.shape[0] - window_size + 1):
            yield board[row:row + window_size, col]  # 4 vertical cells

    # Positive diagonal windows
    for row in range(board.shape[0] - window_size + 1):
        for col in range(board.shape[1] - window_size + 1):
            yield [board[row + i][col + i] for i in range(window_size)]  # Positive diagonal cells

    # Negative diagonal windows
    for row in range(window_size - 1, board.shape[0]):
        for col in range(board.shape[1] - window_size + 1):
            yield [board[row - i][col + i] for i in range(window_size)]  # Negative diagonal cells

def evaluate_window(window, player, opponent):
    """
    Evaluate a window (4 consecutive pieces) for scoring.
    """
    window = np.array(window)  # Convert the window to a numpy array for easier calculations

    player_count = np.count_nonzero(window == player)  # Count player's pieces
    empty_count = np.count_nonzero(window == 0)  # Count empty spaces

    if player_count == 4:
        return 1000  # Win condition
    elif player_count == 3 and empty_count == 1:
        return 100  # Potential win
    elif player_count == 2 and empty_count == 2:
        return 10  # Good position
    return 0
def score_position(board, player):
    """
    Score the board for the given player using windows of consecutive pieces (horizontal, vertical, diagonal).
    """
    score = 0
    opponent = 1 if player == 2 else 2  # Identify opponent

    # Step 1: Prioritize the center column (not part of window checking but important for strategy)
    center_col = board[:, board.shape[1] // 2]
    center_count = list(center_col).count(player)
    score += center_count * 10  # High weight for center control

    # Step 2: Check all windows (horizontal, vertical, and diagonal) for potential 4-in-a-row
    for window in get_windows(board):
        score += evaluate_window(window, player, opponent)

    return score




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

    four_connected = score_position(game_state.board, player)
    opponent_four_connected = score_position(game_state.board, opponent)

    return four_connected -  opponent_four_connected
def easy_evaluation_function(game_state, player):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current GameState and returns a number, where higher numbers are better.
    """

    four_connected = score_position(game_state.board, player)

    return four_connected