"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count number of X's and number of O's
    num_x = 0
    num_o = 0
    for col in board:
        for cell in col:
            if cell == X:
                num_x += 1
            elif cell == O:
                num_o += 1

    # If the board is empty
    if num_x == 0 and num_o == 0:
        return X
    elif num_x > num_o:
        return O
    elif num_x == num_o:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(3):
        for col in range(3):
            cell = board[row][col]
            if cell == EMPTY:
                actions.add((row, col))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Copy the board
    new_board = copy.deepcopy(board)

    # check if the action is legal
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("The action is not a legal move")

    # Get the move of the current player
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_row(row):
        """ 
        Takes a list with 3 cells and returns X if all cells have X, O if all have O and None otherwise
        """
        x_count = 0
        o_count = 0
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
        if x_count == 3:
            return X
        elif o_count == 3:
            return O
        else:
            return None

    # Check the rows to see if they have a 3 in a row
    for row in board:
        result = check_row(row)
        # If the row contained 3 in a row return winner else do nothing
        if result:
            return result

    # check the columns
    for i in range(3):
        col = []
        # For each row in the colum append the righ row
        for row in board:
            col.append(row[i])
        # If the column contained 3 in a row return winner else do nothing
        result = check_row(col)
        if result:
            return result

    # Check the diagonals
    diagonalL = [board[0][0], board[1][1], board[2][2]]
    result = check_row(diagonalL)
    if result:
        return result
    diagonalR = [board[0][2], board[1][1], board[2][0]]
    result = check_row(diagonalR)
    if result:
        return result

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is a winner return True
    if winner(board):
        return True
    # If there are still empty spaces return False, can still add
    for row in board:
        for cell in row:
            if cell == None:
                return False

    # else return True
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If game ended return None
    if terminal(board):
        return None

    def recursive_minimax(board):
        """ best_actions is a list that will go through recursion, can be added from anywhere. Returns the list of optimal actions the player should take."""
        turn = player(board)
        if turn == O:
            best = float("inf")
        else:
            best = float("-inf")
        # Base case
        if terminal(board):
            # No more actions to take, return end utility of board
            return (None, utility(board))
        # Get all the possible actions, uses depth first search
        for action in actions(board):
            path = recursive_minimax(
                result(board, action)
            )
            if turn == O and path[1] < best:
                best = path[1]
                best_action = action
            elif turn == X and path[1] > best:
                best = path[1]
                best_action = action

        return (best_action, best)

    # Else Return the best solution found using recursive function, which is the first in the tuple returned
    return recursive_minimax(board)[0]


