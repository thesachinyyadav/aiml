import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
SQ_SIZE = WIDTH // COLS
LINE_WIDTH = 4
CIRCLE_RADIUS = SQ_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQ_SIZE // 4

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 200, 255)
RED = (255, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - AI Agent")
screen.fill(BLACK)

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
player = 1  # 1: Human, 2: AI
game_over = False
winner = None

def draw_grid():
    for i in range(1, ROWS):
        pygame.draw.line(screen, WHITE, (0, i * SQ_SIZE), (WIDTH, i * SQ_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, (i * SQ_SIZE, 0), (i * SQ_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for r in range(ROWS):
        for c in range(COLS):
            center = (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2)
            if board[r][c] == 1:
                pygame.draw.circle(screen, BLUE, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[r][c] == 2:
                pygame.draw.line(screen, RED, (c * SQ_SIZE + SPACE, r * SQ_SIZE + SPACE),
                                 (c * SQ_SIZE + SQ_SIZE - SPACE, r * SQ_SIZE + SQ_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED, (c * SQ_SIZE + SPACE, r * SQ_SIZE + SQ_SIZE - SPACE),
                                 (c * SQ_SIZE + SQ_SIZE - SPACE, r * SQ_SIZE + SPACE), CROSS_WIDTH)

def display_result(text):
    font = pygame.font.SysFont(None, 40)
    msg = font.render(text, True, BLUE if winner == 1 else RED)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(msg, rect)

def mark_square(r, c, p):
    board[r][c] = p

def is_empty(r, c):
    return board[r][c] == 0

def board_full():
    return all(cell != 0 for row in board for cell in row)

def check_winner(p):
    for i in range(ROWS):
        if all(board[i][j] == p for j in range(COLS)) or all(board[j][i] == p for j in range(ROWS)):
            return True
    if all(board[i][i] == p for i in range(ROWS)) or all(board[i][COLS - i - 1] == p for i in range(ROWS)):
        return True
    return False

def restart():
    global board, player, game_over, winner
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    screen.fill(BLACK)
    draw_grid()
    player = 1
    game_over = False
    winner = None

def minimax(depth, is_max, alpha, beta):
    if check_winner(2): return 1
    if check_winner(1): return -1
    if board_full(): return 0

    if is_max:
        best = -math.inf
        for r in range(ROWS):
            for c in range(COLS):
                if is_empty(r, c):
                    board[r][c] = 2
                    best = max(best, minimax(depth + 1, False, alpha, beta))
                    board[r][c] = 0
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for r in range(ROWS):
            for c in range(COLS):
                if is_empty(r, c):
                    board[r][c] = 1
                    best = min(best, minimax(depth + 1, True, alpha, beta))
                    board[r][c] = 0
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def ai_move():
    best_score = -math.inf
    move = None
    for r in range(ROWS):
        for c in range(COLS):
            if is_empty(r, c):
                board[r][c] = 2
                score = minimax(0, False, -math.inf, math.inf)
                board[r][c] = 0
                if score > best_score:
                    best_score = score
                    move = (r, c)
    if move:
        mark_square(move[0], move[1], 2)

draw_grid()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
            x, y = event.pos
            row, col = y // SQ_SIZE, x // SQ_SIZE
            if is_empty(row, col):
                mark_square(row, col, 1)
                if check_winner(1):
                    winner = 1
                    game_over = True
                else:
                    player = 2
                draw_figures()

    if player == 2 and not game_over:
        ai_move()
        if check_winner(2):
            winner = 2
            game_over = True
        else:
            player = 1
        draw_figures()

    if board_full() and not winner:
        game_over = True

    if game_over:
        if winner:
            display_result(f"Player {winner} Wins!")
        else:
            display_result("It's a Draw!")
    pygame.display.update()
