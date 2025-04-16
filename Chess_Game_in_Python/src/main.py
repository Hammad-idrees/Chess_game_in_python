import sys
import json
import pygame
import threading
from move_history_window import start_move_history_window, move_history  # Shared move_history list
from game import init_board, opponent, make_move, is_game_over
from game import get_move_string
from ui import GameUI, show_instructions
from engine import minimax

# Load configuration from config.json
with open("config.json", "r") as f:
    CONFIG = json.load(f)

def main():
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
    pygame.display.set_caption("Chess Game with AI")
    clock = pygame.time.Clock()

    # Start move history window in a separate thread
    threading.Thread(target=start_move_history_window, daemon=True).start()

    # UI setup
    ui = GameUI(screen, CONFIG["square_size"])
    show_instructions(screen, CONFIG["screen_width"], CONFIG["screen_height"])

    board = init_board()
    turn = "white"  # White starts
    game_over = False

    while not game_over:
        ui.draw_board(board)
        pygame.display.flip()

        over, reason = is_game_over(board, turn)
        if over:
            if reason == "checkmate":
                end_msg = "Checkmate! Black wins!" if turn == "white" else "Checkmate! White wins!"
            else:
                end_msg = "Stalemate! The game is drawn."
            ui.show_end_message(end_msg)
            game_over = True
            continue

        if turn == "white":
            move = ui.get_player_move(board)
            if move is None:
                continue
            board = make_move(board, move)

            # Record move
            move_str = get_move_string(move)
            move_history.append(move_str)
            print("Move history:", move_history)
        else:
            ui.show_message("Computer is thinking...", 2)
            score, move = minimax(board, CONFIG["ai_depth"], -float("inf"), float("inf"), False)
            if move is None:
                ui.show_message("No legal moves available for computer!", 2)
                break
            board = make_move(board, move)

            # Record move
            move_str = get_move_string(move)
            move_history.append(move_str)
            print("Move history:", move_history)

        turn = opponent(turn)
        clock.tick(CONFIG["fps"])

    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nGame interrupted by user.")
