import pygame
import sys
from random import choice

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
GRID_SIZE = 5
CELL_SIZE = 60
XMARGIN = 85
YMARGIN = 100
CELL_GAP = 5
score = 0
click_count = 0

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow
BG_COLOR = (30, 30, 30)
GRID_COLOR = (200, 200, 200)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)
WIN_TEXT_COLOR = (255, 215, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")

font = pygame.font.SysFont(None, 48)
button_font = pygame.font.SysFont(None, 36)

cell_click_sound = pygame.mixer.Sound("Sound/click_234.wav")
win_sound = pygame.mixer.Sound("Sound/win-video-game-sound.wav")
lose_sound = pygame.mixer.Sound("Sound/retro-you-lose-sfx.wav")
pygame.mixer.music.load("Sound/relaxing-chiptune-music.mp3")

win_sound.set_volume(0.1)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = XMARGIN + col * (CELL_SIZE + CELL_GAP)
            y = YMARGIN + row * (CELL_SIZE + CELL_GAP)
            color = grid[row][col] if grid[row][col] is not None else (200, 200, 200)
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)


def handle_click(pos):
    global score, click_count
    x, y = pos
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_x = XMARGIN + col * (CELL_SIZE + CELL_GAP)
            cell_y = YMARGIN + row * (CELL_SIZE + CELL_GAP)
            if cell_x <= x <= cell_x + CELL_SIZE and cell_y <= y <= cell_y + CELL_SIZE:

                next_color = choice(COLORS)

                while any(
                        0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and grid[nr][nc] == next_color
                        for nr, nc in [
                            (row - 1, col),  # Up
                            (row + 1, col),  # Down
                            (row, col - 1),  # Left
                            (row, col + 1),  # Right
                        ]
                ):
                    next_color = choice(COLORS)
                if grid[row][col] is None:
                    grid[row][col] = next_color
                    cell_click_sound.play()
                    score += 10
                else:
                    return

                click_count += 1

                if click_count > 3 and score == 0:
                    return 'lose'


def check_win():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col]
            if color is None:
                return False
    return True


def display_score():
    score_text = f"Score: {score}"
    text = font.render(score_text, True, WIN_TEXT_COLOR)
    text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
    text_y = YMARGIN // 3
    screen.blit(text, (text_x, text_y))


def display_win_message():
    text = font.render("You Win!", True, WIN_TEXT_COLOR)
    text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
    text_y = YMARGIN + 100
    screen.blit(text, (text_x, text_y))
    win_sound.play()


def display_lose_message():
    text = font.render("You Lose!", True, WIN_TEXT_COLOR)
    text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
    text_y = YMARGIN + 100
    screen.blit(text, (text_x, text_y))
    lose_sound.play()


def draw_button(text, x, y, width, height, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    text_surf = button_font.render(text, True, BUTTON_TEXT_COLOR)
    screen.blit(text_surf, (x + (width - text_surf.get_width()) // 2, y + (height - text_surf.get_height()) // 2))
    return pygame.Rect(x, y, width, height)


def reset_game():
    global grid, score, click_count
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Reset the grid to empty
    score = 0
    click_count = 0


def pre_game_menu():
    running = True
    while running:
        screen.fill(BG_COLOR)

        title = font.render("Color Fill Puzzle", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, YMARGIN // 2))

        start_button_rect = draw_button("Start Game", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50, 160, 50)
        exit_button_rect = draw_button("Exit", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 20, 100, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    running = False
                elif exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def main():
    pre_game_menu()

    running = True
    game_won = False
    game_lost = False
    new_game_button_rect = None
    exit_button_rect = None

    while running:
        screen.fill(BG_COLOR)

        draw_grid()
        display_score()

        if game_won:
            display_win_message()
        elif game_lost:
            display_lose_message()

        if game_won:
            new_game_button_rect = draw_button("New Game", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)
            exit_button_rect = draw_button("Exit", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 70, 100, 50)
        elif game_lost:
            new_game_button_rect = draw_button("New Game", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)
            exit_button_rect = draw_button("Exit", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 70, 100, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_won:
                if new_game_button_rect and new_game_button_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_won = False
                elif exit_button_rect and exit_button_rect.collidepoint(mouse_pos):
                    running = False
            elif game_lost:
                if new_game_button_rect and new_game_button_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_lost = False
                elif exit_button_rect and exit_button_rect.collidepoint(mouse_pos):
                    running = False
            else:
                result = handle_click(mouse_pos)

                if result == 'lose':
                    game_lost = True
                elif check_win():
                    game_won = True

    pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
