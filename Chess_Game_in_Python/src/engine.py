from game import generate_moves, make_move, piece_values

def evaluate_board(board):
    score = 0
    for row in board:
        for piece in row:
            score += piece_values.get(piece, 0)
    return score

def minimax(board, depth, alpha, beta, maximizing):
    color = "white" if maximizing else "black"
    legal_moves = generate_moves(board, color)
    if depth == 0 or not legal_moves:
        return evaluate_board(board), None

    best_move = None
    if maximizing:
        max_eval = -float("inf")
        for move in legal_moves:
            new_board = make_move(board, move)
            eval_score, _ = minimax(new_board, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in legal_moves:
            new_board = make_move(board, move)
            eval_score, _ = minimax(new_board, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move
