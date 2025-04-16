import copy

# Pieces values and board evaluation values are used in engine.py too.
piece_values = {
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
    'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000,
    '.': 0
}

def init_board():
    """Initialize the chess board."""
    board = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ]
    return board

# Helper functions
def on_board(row, col):
    return 0 <= row < 8 and 0 <= col < 8

def get_piece_color(piece):
    if piece == '.':
        return None
    return "white" if piece.isupper() else "black"

def opponent(color):
    return "black" if color == "white" else "white"

# -----------------------------------------------------------------------------
# Move Generation and Handling
# -----------------------------------------------------------------------------

def generate_moves(board, color):
    moves = []
    directions = {
        'N': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)],
        'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        'R': [(-1, 0), (1, 0), (0, -1), (0, 1)],
        'Q': [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)],
        'K': [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    }
    
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == '.' or get_piece_color(piece) != color:
                continue
            start = (i, j)
            # Pawn moves
            if piece.upper() == 'P':
                d = -1 if color == "white" else 1
                next_row = i + d
                if on_board(next_row, j) and board[next_row][j] == '.':
                    moves.append((start, (next_row, j)))
                    if (color == "white" and i == 6) or (color == "black" and i == 1):
                        next_row2 = i + 2*d
                        if on_board(next_row2, j) and board[next_row2][j] == '.':
                            moves.append((start, (next_row2, j)))
                for dj in [-1, 1]:
                    next_col = j + dj
                    if on_board(next_row, next_col):
                        target = board[next_row][next_col]
                        if target != '.' and get_piece_color(target) == opponent(color):
                            moves.append((start, (next_row, next_col)))
            # Knight moves
            elif piece.upper() == 'N':
                for d in directions['N']:
                    ni, nj = i + d[0], j + d[1]
                    if on_board(ni, nj):
                        target = board[ni][nj]
                        if target == '.' or get_piece_color(target) == opponent(color):
                            moves.append((start, (ni, nj)))
            # Bishop moves
            elif piece.upper() == 'B':
                for d in directions['B']:
                    ni, nj = i, j
                    while True:
                        ni += d[0]
                        nj += d[1]
                        if not on_board(ni, nj):
                            break
                        target = board[ni][nj]
                        if target == '.':
                            moves.append((start, (ni, nj)))
                        else:
                            if get_piece_color(target) == opponent(color):
                                moves.append((start, (ni, nj)))
                            break
            # Rook moves
            elif piece.upper() == 'R':
                for d in directions['R']:
                    ni, nj = i, j
                    while True:
                        ni += d[0]
                        nj += d[1]
                        if not on_board(ni, nj):
                            break
                        target = board[ni][nj]
                        if target == '.':
                            moves.append((start, (ni, nj)))
                        else:
                            if get_piece_color(target) == opponent(color):
                                moves.append((start, (ni, nj)))
                            break
            # Queen moves
            elif piece.upper() == 'Q':
                for d in directions['Q']:
                    ni, nj = i, j
                    while True:
                        ni += d[0]
                        nj += d[1]
                        if not on_board(ni, nj):
                            break
                        target = board[ni][nj]
                        if target == '.':
                            moves.append((start, (ni, nj)))
                        else:
                            if get_piece_color(target) == opponent(color):
                                moves.append((start, (ni, nj)))
                            break
            # King moves including simplified castling
            elif piece.upper() == 'K':
                for d in directions['K']:
                    ni, nj = i + d[0], j + d[1]
                    if on_board(ni, nj):
                        target = board[ni][nj]
                        if target == '.' or get_piece_color(target) == opponent(color):
                            moves.append((start, (ni, nj)))
                if color == "white" and i == 7 and j == 4 and board[7][4] == 'K':
                    if board[7][5] == '.' and board[7][6] == '.' and board[7][7] == 'R':
                        moves.append((start, (7, 6)))
                    if board[7][3] == '.' and board[7][2] == '.' and board[7][1] == '.' and board[7][0] == 'R':
                        moves.append((start, (7, 2)))
                elif color == "black" and i == 0 and j == 4 and board[0][4] == 'k':
                    if board[0][5] == '.' and board[0][6] == '.' and board[0][7] == 'r':
                        moves.append((start, (0, 6)))
                    if board[0][3] == '.' and board[0][2] == '.' and board[0][1] == '.' and board[0][0] == 'r':
                        moves.append((start, (0, 2)))
    
    legal_moves = []
    for move in moves:
        new_board = make_move(board, move)
        if not is_in_check(new_board, color):
            legal_moves.append(move)
    return legal_moves

def make_move(board, move):
    new_board = copy.deepcopy(board)
    (start, end) = move
    piece = new_board[start[0]][start[1]]
    new_board[end[0]][end[1]] = piece
    new_board[start[0]][start[1]] = '.'
    
    # Pawn promotion automatically to Queen
    if piece == 'P' and end[0] == 0:
        new_board[end[0]][end[1]] = 'Q'
    if piece == 'p' and end[0] == 7:
        new_board[end[0]][end[1]] = 'q'
    
    # Handle castling
    if piece.upper() == 'K' and abs(end[1] - start[1]) == 2:
        if end[1] > start[1]:
            rook_start = (start[0], 7)
            rook_end = (start[0], end[1] - 1)
        else:
            rook_start = (start[0], 0)
            rook_end = (start[0], end[1] + 1)
        new_board[rook_end[0]][rook_end[1]] = new_board[rook_start[0]][rook_start[1]]
        new_board[rook_start[0]][rook_start[1]] = '.'
    return new_board

def is_in_check(board, color):
    king = 'K' if color == "white" else 'k'
    king_pos = None
    for i in range(8):
        for j in range(8):
            if board[i][j] == king:
                king_pos = (i, j)
                break
        if king_pos:
            break
    if king_pos is None:
        return True

    opp_color = opponent(color)
    opp_moves = generate_pseudo_legal_moves(board, opp_color)
    for move in opp_moves:
        if move[1] == king_pos:
            return True
    return False

def generate_pseudo_legal_moves(board, color):
    moves = []
    directions = {
        'N': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)],
        'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        'R': [(-1, 0), (1, 0), (0, -1), (0, 1)],
        'Q': [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)],
        'K': [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    }
    
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == '.' or get_piece_color(piece) != color:
                continue
            start = (i, j)
            if piece.upper() == 'P':
                d = -1 if color == "white" else 1
                next_row = i + d
                if on_board(next_row, j):
                    if board[next_row][j] == '.':
                        moves.append((start, (next_row, j)))
                    for dj in [-1, 1]:
                        next_col = j + dj
                        if on_board(next_row, next_col):
                            target = board[next_row][next_col]
                            if target != '.' and get_piece_color(target) == opponent(color):
                                moves.append((start, (next_row, next_col)))
            elif piece.upper() == 'N':
                for d in directions['N']:
                    ni, nj = i + d[0], j + d[1]
                    if on_board(ni, nj):
                        moves.append((start, (ni, nj)))
            elif piece.upper() == 'B':
                for d in directions['B']:
                    ni, nj = i, j
                    while True:
                        ni += d[0]
                        nj += d[1]
                        if not on_board(ni, nj):
                            break
                        moves.append((start, (ni, nj)))
                        if board[ni][nj] != '.':
                            break
            elif piece.upper() == 'R':
                for d in directions['R']:
                    ni, nj = i, j
                    while True:
                        ni += d[0]
                        nj += d[1]
                        if not on_board(ni, nj):
                            break
                        moves.append((start, (ni, nj)))
                        if board[ni][nj] != '.':
                            break
            elif piece.upper() == 'Q':
                for d in directions['Q']:
                    ni, nj = i, j
                    while True:
                        ni += d[0]
                        nj += d[1]
                        if not on_board(ni, nj):
                            break
                        moves.append((start, (ni, nj)))
                        if board[ni][nj] != '.':
                            break
            elif piece.upper() == 'K':
                for d in directions['K']:
                    ni, nj = i + d[0], j + d[1]
                    if on_board(ni, nj):
                        moves.append((start, (ni, nj)))
    return moves

def is_game_over(board, color):
    moves = generate_moves(board, color)
    if not moves:
        if is_in_check(board, color):
            return True, "checkmate"
        else:
            return True, "stalemate"
    return False, None

# For text input fallback (if needed for console debug)
def user_move_text():
    move_input = input("Enter your move (e.g. e2e4): ").strip()
    if len(move_input) < 4:
        return None
    start = (8 - int(move_input[1]), ord(move_input[0].lower()) - ord('a'))
    end   = (8 - int(move_input[3]), ord(move_input[2].lower()) - ord('a'))
    return (start, end)

# ALgebraic to index
def algebraic_to_index(algebraic):
    # Example: 'e2' -> (6, 4)
    row = 8 - int(algebraic[1])
    col = ord(algebraic[0]) - ord('a')
    return row, col

# index to Algebraic
def index_to_algebraic(row, col):
    """
    Converts board indices to algebraic notation.
    Example: (6, 4) -> 'e2'
    """
    return f"{chr(col + ord('a'))}{8 - row}"

# get move string we insert here
def get_move_string(move):
    """
    Converts a move (a tuple ((start_row, start_col), (end_row, end_col)))
    into algebraic notation.
    Example: ((6, 4), (4, 4)) -> 'e2e4'
    """
    start, end = move
    return index_to_algebraic(start[0], start[1]) + index_to_algebraic(end[0], end[1])