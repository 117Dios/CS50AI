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
    counter = 0
    
    for list in board:
        for cell in list:
            if cell != EMPTY:
                counter += 1
    
    if counter % 2 == 0:
        return X
    else:
        return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    if terminal(board):
        return "Game is over"
    
    actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    i, j = action
    
    if i > 2 or i < 0 or j > 2 or j < 0:
        raise Exception("Out of bounds")
    
    copied_board = copy.deepcopy(board)
    
    if copied_board[i][j] != EMPTY:
        raise Exception("Invalid Action")
    else:
        
        copied_board[i][j] = player(board)
        
        return copied_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for row in board:    
        if row[0] is not EMPTY and all(cell == row[0] for cell in row):
            return row[0]  
               
    for j in range(3):         
        if board[0][j] is not EMPTY and all(row[j] == board[0][j] for row in board):
            return board[0][j]
        
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[2][0] is not EMPTY and board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]
    else:
        return None
    
                
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    win = winner(board)
    
    if all(cells != EMPTY for row in board for cells in row) or win is not None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    match winner(board):
        case "X":
            return 1
        case "O":
            return -1
        case _:
            return 0        


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return None    
    
    if player(board) == X: 
        return maxvalue(board)[1]
 
    if player(board) == O: 
        return minvalue(board)[1]
    

def maxvalue(board):
    
    if terminal(board):
        return utility(board), None
    
    value = -math.inf
    
    for action in actions(board):
        temp_value = max(value, minvalue(result(board, action))[0])
        if temp_value > value:
            value = temp_value
            best_action = action
    
    return value, best_action


def minvalue(board):
    
    if terminal(board):
        return utility(board), None
    
    value = math.inf
    
    for action in actions(board):
        temp_value = min(value, maxvalue(result(board, action))[0])
        if temp_value < value:
            value = temp_value
            best_action = action
    
    return value, best_action