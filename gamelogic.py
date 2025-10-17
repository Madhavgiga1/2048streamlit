"""
Game Logic for 2048
Pure functional programming - no side effects
"""
import random
import copy

def initialize_board(size=4):
    """Create empty board and add 2 random tiles"""
    board = [[0] * size for _ in range(size)]
    board = add_random_tile(board)
    board = add_random_tile(board)
    return board

def add_random_tile(board):
    """Add random 2 or 4 to empty cell"""
    empty_cells = [(i, j) for i in range(len(board)) 
                   for j in range(len(board[0])) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4
    return board

def slide_row(row):
    """Slide and merge single row to left"""
    # Remove zeros
    non_zero = [num for num in row if num != 0]
    
    # Merge adjacent equal numbers
    merged = []
    score = 0
    i = 0
    while i < len(non_zero):
        if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
            merged.append(non_zero[i] * 2)
            score += non_zero[i] * 2
            i += 2
        else:
            merged.append(non_zero[i])
            i += 1
    
    # Pad with zeros
    merged += [0] * (len(row) - len(merged))
    return merged, score

def move_left(board):
    """Move all tiles left"""
    new_board = []
    total_score = 0
    for row in board:
        new_row, score = slide_row(row)
        new_board.append(new_row)
        total_score += score
    return new_board, total_score

def move_right(board):
    """moving all tiles right"""
    new_board = []
    total_score = 0
    for row in board:
        reversed_row = row[::-1]
        new_row, score = slide_row(reversed_row)
        new_board.append(new_row[::-1])
        total_score += score
    return new_board, total_score

def transpose(board):
    """Transpose board"""
    """sort of like rotating the board 90 degree without reversal"""
    size = len(board)
    return [[board[j][i] for j in range(size)] for i in range(size)]

def move_up(board):
    """mobving all tiles up and returns a tuple"""
    """row becomes column and column becomes row"""
    transposed = transpose(board)
    moved, score = move_left(transposed)
    return transpose(moved), score

def move_down(board):
    """moving all  the tiles down"""
    transposed = transpose(board)
    moved, score = move_right(transposed)
    return transpose(moved), score

def board_changed(old_board, new_board):
    """to check if board changed after move"""
    """only when the board changes we can add a new tile"""
    return old_board != new_board

def can_move(board):
    """to check if any move is possible"""
    size = len(board)
    
   
    for row in board:
        if 0 in row:
            return True
    
    # checking for adjacent equal numbers horizontally
    for i in range(size):
        for j in range(size - 1):
            if board[i][j] == board[i][j + 1]:
                return True
    
    # checking for adjacent equal numbers vertically
    for i in range(size - 1):
        for j in range(size):
            if board[i][j] == board[i + 1][j]:
                return True
    
    return False

def has_won(board):
    """to check if a 2048 tile exists in the board till now """
    for row in board:
        if 2048 in row:
            return True
    return False

def get_game_state(board):
    """ current game state"""
    if has_won(board):
        return "WON"
    elif not can_move(board):
        return "LOST"
    else:
        return "PLAYING"