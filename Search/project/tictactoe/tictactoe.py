"""
Tic Tac Toe Player
"""

import math
import copy
from shutil import move

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
    # count the occurence of each sign
    numX = sum([row.count('X') for row in board])
    numO = sum([row.count('O') for row in board])
    numEmpty = 9-numX-numO
    # return the player
    if numEmpty == 0 :
        return None
    if numX == numO :
        return X
    else :
        return O

def countEmpty(board):
    """
    Returns the number of empty cell in a board.
    """
    return sum([row.count(EMPTY) for row in board])

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # check all the empty place
    positions = []
    for i in range(len(board)):
        for j,val in enumerate(board[i]):
            if val is None:
                positions.append((i,j))
    # return None if there is no possible action
    if len(positions) == 0:
        return None
    return positions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception('Impossible Action')
    
    turn = player(board)
    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = turn 

    return newBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winX = [X,X,X]
    winO = [O,O,O]

    if winX in board or winX in [[board[i][j] for i in range(3)] for j in range(3)] or winX == [board[i][i] for i in range(3)] or winX == [board[2-i][i] for i in range(3)] :
        return  X
    if winO in board or winO in [[board[i][j] for i in range(3)] for j in range(3)] or winO == [board[i][i] for i in range(3)] or winO == [board[2-i][i] for i in range(3)] :
        return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if actions(board) is None or winner(board) is not None :
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O :
        return -1
    else :
        return 0

def maxValue(board):
    """
    Returns the maximal value in a board with all the actions.
    The real utility is compute with the number of empty cell in the board to have the fastest solution
    """
    if terminal(board):
        return utility(board)*(countEmpty(board)+1)
    value = -math.inf
    for a in actions(board):
        value = max(value,minValue(result(board,a)))
    return value


def minValue(board):
    """
    Returns the minimal value for all action possible in a board.
    The real utility is compute with the number of empty cell in the board to have the fastest solution
    """
    if terminal(board):
        return utility(board)*(countEmpty(board)+1)
    value = math.inf
    for a in actions(board):
        value = min(value,maxValue(result(board,a)))
    return value


# This will return the best possible move for the player
def minimax(board) :
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        bestVal = -math.inf
        bestMove = None

        for a in actions(board):
            moveVal = minValue(result(board,a))
            if (moveVal > bestVal) :               
                bestMove = a
                bestVal = moveVal

    elif player(board) == O:
        bestVal = math.inf
        bestMove = None

        for a in actions(board):

            moveVal = maxValue(result(board,a))
            if (moveVal < bestVal) :               
                bestMove = a
                bestVal = moveVal
    return bestMove