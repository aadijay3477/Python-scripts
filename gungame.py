import cv2
import numpy as np
import pytesseract
import pygetwindow as gw
import pywinauto
import pyautogui
import time
import random

ORIGINAL_TITLE = 'Doomsday: Last Survivors'
TIME_VARIATION = 0.003

# Initialize Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Python312\Scripts\pytesseract.exe'  # Update with your Tesseract path

# Game board parameters
x_start, y_start = 360, 75  # Top-left corner
x_end, y_end = 1005, 718    # Bottom-right corner
cell_width = (x_end - x_start) / 4
cell_height = (y_end - y_start) / 4

# Function to generate random sleep time with a small variation
def random_sleep(base_time):
    variation = random.uniform(-TIME_VARIATION * base_time, TIME_VARIATION * base_time)
    time.sleep(base_time + variation)

# Activate the game window
def activate_window(window):
    try:
        pywinauto.Application().connect(handle=window._hWnd).top_window().set_focus()
        random_sleep(0.155)
    except Exception as e:
        print(f"Error activating window: {e}")

# OCR function for extracting numbers from a cell image
def extract_number_from_cell(cell_img):
    number_region = cell_img[int(0.7 * cell_height):, int(0.7 * cell_width):]
    number_text = pytesseract.image_to_string(number_region, config='--psm 7')
    try:
        return int(number_text.strip())
    except ValueError:
        return 0  # Return 0 if no valid number is detected

# Capture the game board
def capture_game_board():
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

# Extract the grid of numbers from the board
def detect_grid(img):
    grid = np.zeros((4, 4), dtype=int)  # Initialize 4x4 grid
    for i in range(4):
        for j in range(4):
            x1 = int(x_start + j * cell_width)
            y1 = int(y_start + i * cell_height)
            x2 = int(x1 + cell_width)
            y2 = int(y1 + cell_height)
            cell_img = img[y1:y2, x1:x2]
            detected_number = extract_number_from_cell(cell_img)
            grid[i][j] = detected_number
    return grid

# Check if merging is possible in a specific direction
def can_merge(grid, direction):
    if direction == 'up':
        return any(grid[i][j] == grid[i - 1][j] for i in range(1, 4) for j in range(4) if grid[i][j] != 0)
    elif direction == 'down':
        return any(grid[i][j] == grid[i + 1][j] for i in range(2) for j in range(4) if grid[i][j] != 0)
    elif direction == 'left':
        return any(grid[i][j] == grid[i][j - 1] for j in range(1, 4) for i in range(4) if grid[i][j] != 0)
    elif direction == 'right':
        return any(grid[i][j] == grid[i][j + 1] for j in range(3) for i in range(4) if grid[i][j] != 0)
    return False

# Count empty cells and calculate potential merges
def evaluate_move(grid, direction):
    new_grid = np.copy(grid)
    empty_cells = 0
    merge_possible = False

    # Move logic based on direction
    if direction == 'up':
        for j in range(4):
            for i in range(1, 4):
                if new_grid[i][j] != 0:
                    if new_grid[i - 1][j] == 0:
                        new_grid[i - 1][j] = new_grid[i][j]
                        new_grid[i][j] = 0
                    elif new_grid[i - 1][j] == new_grid[i][j]:
                        new_grid[i - 1][j] *= 2
                        new_grid[i][j] = 0
                        merge_possible = True
    elif direction == 'down':
        for j in range(4):
            for i in range(2, -1, -1):
                if new_grid[i][j] != 0:
                    if new_grid[i + 1][j] == 0:
                        new_grid[i + 1][j] = new_grid[i][j]
                        new_grid[i][j] = 0
                    elif new_grid[i + 1][j] == new_grid[i][j]:
                        new_grid[i + 1][j] *= 2
                        new_grid[i][j] = 0
                        merge_possible = True
    elif direction == 'left':
        for i in range(4):
            for j in range(1, 4):
                if new_grid[i][j] != 0:
                    if new_grid[i][j - 1] == 0:
                        new_grid[i][j - 1] = new_grid[i][j]
                        new_grid[i][j] = 0
                    elif new_grid[i][j - 1] == new_grid[i][j]:
                        new_grid[i][j - 1] *= 2
                        new_grid[i][j] = 0
                        merge_possible = True
    elif direction == 'right':
        for i in range(4):
            for j in range(2, -1, -1):
                if new_grid[i][j] != 0:
                    if new_grid[i][j + 1] == 0:
                        new_grid[i][j + 1] = new_grid[i][j]
                        new_grid[i][j] = 0
                    elif new_grid[i][j + 1] == new_grid[i][j]:
                        new_grid[i][j + 1] *= 2
                        new_grid[i][j] = 0
                        merge_possible = True

    empty_cells = np.count_nonzero(new_grid == 0)
    return empty_cells, merge_possible

# Perform move with optimized strategy
def perform_move(grid):
    possible_moves = ['up', 'down', 'left', 'right']
    move_scores = {}

    for move in possible_moves:
        if can_merge(grid, move):
            empty_cells, merge_possible = evaluate_move(grid, move)
            move_scores[move] = empty_cells + (10 if merge_possible else 0)

    if move_scores:
        best_move = max(move_scores, key=move_scores.get)
        return best_move
    return None

# Simulate the move using pyautogui
def perform_optimized_move(direction):
    x_center = (x_start + x_end) // 2
    y_center = (y_start + y_end) // 2
    offset = 200  # Amount to drag

    move_dict = {
        'up': (0, -offset),
        'down': (0, offset),
        'left': (-offset, 0),
        'right': (offset, 0),
    }

    if direction in move_dict:
        pyautogui.moveTo(x_center, y_center)
        pyautogui.drag(*move_dict[direction], duration=0.2)

# Main game loop
def play_game():
    while True:
        game_board_img = capture_game_board()
        grid = detect_grid(game_board_img)
        print("Detected Grid:")
        print(grid)

        best_move = perform_move(grid)

        if best_move:
            print(f"Performing move: {best_move}")
            perform_optimized_move(best_move)
        else:
            print("No more possible moves. Game over.")
            break

        time.sleep(1)

# Start the game loop
if __name__ == "__main__":
    windows = gw.getWindowsWithTitle(ORIGINAL_TITLE)
    if windows:
        activate_window(windows[0])
        play_game()
    else:
        print(f"No windows found with title: {ORIGINAL_TITLE}")
