## it's incomplete

import pyautogui
import time
import pygetwindow as gw
import keyboard
import random

# Constants for offsets and random variation
PIXEL_OFFSET = 5
TIME_VARIATION = 0.003
MAX_LIMIT_HEAL = 300
MAX_WAIT_TIME = 26 * 60  # 26 minutes in seconds
MIN_WAIT_TIME = 60  # 1 minute in seconds

IMAGE_PATH = {
    'search-icon': './Assets/hive/Screen_20240603170954.png',
    'search-button': './Assets/hive/Screen_20240603171021.png',
    'rally-button': './Assets/hive/Screen_20240603171021.png',
    'already launched': './Assets/hive/',
    'march-button': './Assets/hive/Screen_20240603171327',
}

# Function to click at a specific position with a random offset
def click(x, y, duration=0.0):
    offset_x = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
    offset_y = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
    pyautogui.moveTo(x + offset_x, y + offset_y, duration)
    pyautogui.mouseDown()
    time.sleep(duration)
    pyautogui.mouseUp()

# Function to generate random sleep time with a small variation
def random_sleep(base_time):
    variation = random.uniform(-TIME_VARIATION * base_time, TIME_VARIATION * base_time)
    time.sleep(base_time + variation)

# Function to handle additional logic for troop-type image
def handle_troop_type(center, duration):
    click(center.x + 390, center.y + 11, duration)  # Adjust click position

# Function to perform random mouse movements
def random_mouse_movement():
    x, y = pyautogui.position()
    new_x = x + random.randint(-100, 100)
    new_y = y + random.randint(-100, 100)
    pyautogui.moveTo(new_x, new_y, duration=random.uniform(0.1, 0.3))

# Function to find and click the image
def find_and_click_image(image_key, duration, max_wait=0):
    image_path = IMAGE_PATH[image_key]
    print(f"Looking for image: {image_key}")  # Print the image path key
    start_time = time.time()

    while True:
        for confidence_threshold in range(10, 3, -1):
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=(confidence_threshold / 10.0))
                if location is not None:
                    center = pyautogui.center(location)
                    print(f"Image found at: {location}, center at: {center}, confidence: {(confidence_threshold / 10.0)}")
                    # Handle specific logic for troop-type image
                    if image_key == 'troop-type':
                        handle_troop_type(center, duration)
                    else:
                        click(center.x, center.y, duration)
                    print(f"Clicked on the image at {center}.")
                    return True
            except pyautogui.ImageNotFoundException:
                print(f"Image not found for confidence level: {(confidence_threshold / 10.0)}")
            except Exception as e:
                print(f"An error occurred: {e}")

        if max_wait and (time.time() - start_time) > max_wait:
            print(f"Image {image_key} not found within the max wait time of {max_wait} seconds")
            return False
        random_sleep(1)  # Add a small delay before retrying
        # random_mouse_movement()  # Perform random mouse movement

# Activate the game window
def activate_window():
    try:
        win = gw.getWindowsWithTitle('Doomsday: Last Survivors')[0]
        win.activate()
        random_sleep(0.533)  # Adjusted for the initial sleeps
    except IndexError:
        print("Window not found!")

# Main function to run the macro
def run_macro():
    new_variable = 0

    while new_variable < MAX_LIMIT_HEAL:
        if keyboard.is_pressed('F8'):
            print("F8 pressed, stopping the macro.")
            break