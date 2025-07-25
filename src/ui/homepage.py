from choose_word import choose_word
from validate import validate
from choose_word import WORDLE_WORDS
import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 124, 126)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
RED = (200,0,0)

BOX_SIZE = 60
BOX_MARGIN = 15
START_X = 10
START_Y = 10

WIDTH, HEIGHT = 380, 640

def run():
    KEYBOARD_ROWS = [
        list("QWERTYUIOP"),
        list("ASDFGHJKL"),
        list("ZXCVBNM")
    ]
    KEY_SIZE = 32
    KEY_MARGIN = 6
    KEY_START_Y = HEIGHT - 3 * (KEY_SIZE + KEY_MARGIN) - 40

    key_colors = {}
    for row in KEYBOARD_ROWS:
        for k in row:
            key_colors[k] = None

    def draw_keyboard():
        for row_idx, row in enumerate(KEYBOARD_ROWS):
            row_len = len(row)
            total_width = row_len * KEY_SIZE + (row_len - 1) * KEY_MARGIN
            start_x = (WIDTH - total_width) // 2
            y = KEY_START_Y + row_idx * (KEY_SIZE + KEY_MARGIN)
            for col_idx, key in enumerate(row):
                x = start_x + col_idx * (KEY_SIZE + KEY_MARGIN)
                color = key_colors[key]
                if color == 1:
                    box_color = GREEN
                elif color == 0:
                    box_color = YELLOW
                elif color == -1:
                    box_color = DARK_GRAY
                else:
                    box_color = WHITE
                pygame.draw.rect(SCREEN, box_color, (x, y, KEY_SIZE, KEY_SIZE))
                pygame.draw.rect(SCREEN, BLACK, (x, y, KEY_SIZE, KEY_SIZE), 2)
                key_surface = FONT.render(key, True, BLACK)
                key_rect = key_surface.get_rect(center=(x + KEY_SIZE // 2, y + KEY_SIZE // 2))
                SCREEN.blit(key_surface, key_rect)
    pygame.init()
    
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wordle")
    FONT = pygame.font.SysFont(None, 48)

    answer = choose_word()

    color_matrix = [[None]*5 for _ in range(6)]

    def draw_boxes(startX, startY, letters_row, color_row):
        for i in range(5):
            x = startX + i * (BOX_SIZE + BOX_MARGIN)
            if color_row and color_row[i] == 1:
                box_color = (106, 170, 100)  
            elif color_row and color_row[i] == 0:
                box_color = (201, 180, 88)  
            elif color_row and color_row[i] == -1:
                box_color = (120, 124, 126)  
            else:
                box_color = WHITE
            pygame.draw.rect(SCREEN, box_color, (x, startY, BOX_SIZE, BOX_SIZE))
            pygame.draw.rect(SCREEN, BLACK, (x, startY, BOX_SIZE, BOX_SIZE), 3)
            if letters_row[i]:
                char_surface = FONT.render(letters_row[i], True, BLACK if box_color == WHITE else WHITE)
                char_rect = char_surface.get_rect(center=(x + BOX_SIZE // 2, startY + BOX_SIZE // 2))
                SCREEN.blit(char_surface, char_rect)

    letters_list = [[""] * 5 for _ in range(6)]
    current_row = 0
    current_index = 0
    game_over = False
    win = False
    clock = pygame.time.Clock()
    invalid_word = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not game_over:
                if pygame.K_a <= event.key <= pygame.K_z and current_index < 5:
                    letters_list[current_row][current_index] = event.unicode.upper()
                    current_index += 1
                    invalid_word = False
                elif event.key == pygame.K_BACKSPACE and current_index > 0:
                    current_index -= 1
                    letters_list[current_row][current_index] = ""
                    invalid_word = False
                elif event.key == pygame.K_RETURN and current_index == 5:
                    guess = "".join(letters_list[current_row])
                    if guess not in WORDLE_WORDS:
                        invalid_word = True
                    else:
                        result = validate(guess, answer)
                        color_matrix[current_row] = result

                        for idx, char in enumerate(guess):
                            prev = key_colors.get(char, None)
                            if result[idx] == 1:
                                key_colors[char] = 1
                            elif result[idx] == 0 and prev != 1:
                                key_colors[char] = 0
                            elif result[idx] == -1 and prev not in (1,0):
                                key_colors[char] = -1
                        if guess == answer:
                            game_over = True
                            win = True
                        elif current_row == 5:
                            game_over = True
                        else:
                            current_row += 1
                            current_index = 0
                        invalid_word = False

        SCREEN.fill(WHITE)
        for i in range(6):
            y = START_Y + i * (BOX_SIZE + BOX_MARGIN)
            draw_boxes(START_X, y, letters_list[i], color_matrix[i])
        draw_keyboard()
        if game_over:
            msg = "You Win!" if win else f"Lose! Answer: {answer}"
            text = FONT.render(msg, True, GREEN if win else RED)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 10))
            SCREEN.blit(text, rect)
        elif invalid_word:
            msg = "Invalid word!"
            text = FONT.render(msg, True, RED)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 10))
            SCREEN.blit(text, rect)
        pygame.display.flip()
        clock.tick(60)