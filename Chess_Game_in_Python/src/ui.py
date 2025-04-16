import pygame
from game import algebraic_to_index, make_move, generate_moves

# Define colors
WHITE = (245, 245, 220)
BLACK = (139, 69, 19)
HIGHLIGHT = (186, 202, 68)
MESSAGE_BG = (50, 50, 50)
MESSAGE_FG = (255, 255, 255)

def load_piece_images(square_size):
    pieces = {}
    piece_ids = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK',
                 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    for pid in piece_ids:
        try:
            image = pygame.image.load(f"assets/images/{pid}.png")
            pieces[pid] = pygame.transform.scale(image, (square_size, square_size))
        except Exception as e:
            print(f"Error loading {pid}.png: {e}")
    return pieces

class GameUI:
    def __init__(self, screen, square_size):
        self.screen = screen
        self.square_size = square_size
        self.piece_images = load_piece_images(square_size)
        self.selected_square = None
        self.possible_moves = []

    def draw_board(self, board):
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                rect = pygame.Rect(col * self.square_size, row * self.square_size,
                                   self.square_size, self.square_size)
                pygame.draw.rect(self.screen, color, rect)

                if self.selected_square and (row, col) == self.selected_square:
                    pygame.draw.rect(self.screen, HIGHLIGHT, rect, 4)

                piece = board[row][col]
                if piece != '.':
                    img_key = ("w" if piece.isupper() else "b") + piece.upper()
                    if img_key in self.piece_images:
                        self.screen.blit(self.piece_images[img_key], rect)
                    else:
                        font = pygame.font.SysFont("arial", 36)
                        text = font.render(piece, True, (0, 0, 0))
                        self.screen.blit(text, rect)

    def get_square_under_mouse(self):
        pos = pygame.mouse.get_pos()
        col = pos[0] // self.square_size
        row = pos[1] // self.square_size
        return (row, col)

    def get_player_move(self, board):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = self.get_square_under_mouse()
                if self.selected_square is None:
                    piece = board[row][col]
                    if piece != '.' and piece.isupper():
                        self.selected_square = (row, col)
                        self.possible_moves = [
                            move for move in generate_moves(board, "white")
                            if move[0] == self.selected_square
                        ]
                else:
                    dest_square = (row, col)
                    for m in self.possible_moves:
                        if m[1] == dest_square:
                            move = m
                            break
                    self.selected_square = None
                    self.possible_moves = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from game import user_move_text
                    move = user_move_text()
        return move

    def show_message(self, message, delay_sec=1):
        font = pygame.font.SysFont("arial", 32)
        text = font.render(message, True, MESSAGE_FG)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2,
                                          self.screen.get_height() // 2))
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        s.set_alpha(180)
        s.fill(MESSAGE_BG)
        self.screen.blit(s, (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(delay_sec * 1000)

    def show_end_message(self, message):
        font = pygame.font.SysFont("arial", 40)
        text = font.render(message, True, MESSAGE_FG)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2,
                                          self.screen.get_height() // 2))
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        s.set_alpha(200)
        s.fill(MESSAGE_BG)
        self.screen.blit(s, (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False

    def draw_move_history(self, move_history, font_size=20):
        font = pygame.font.SysFont("arial", font_size)
        x_offset = self.screen.get_width() - 150
        y_offset = 10
        background_rect = pygame.Rect(x_offset - 5, y_offset - 5,
                                      140, self.screen.get_height() - 20)
        pygame.draw.rect(self.screen, (50, 50, 50), background_rect)
        for move in move_history:
            text = font.render(move, True, (255, 255, 255))
            self.screen.blit(text, (x_offset, y_offset))
            y_offset += font_size + 5

def show_instructions(screen, width, height):
    instructions = [
        "Welcome to Chess with AI!",
        "",
        "HOW TO PLAY:",
        " - You are playing as WHITE.",
        " - Click on a white piece to select it.",
        " - Click on a destination square to move.",
        " - Legal moves are highlighted.",
        "",
        "Press any key to start the game."
    ]
    font = pygame.font.SysFont("arial", 28)
    screen.fill((30, 30, 30))

    y_offset = height // 4
    for line in instructions:
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 40

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
