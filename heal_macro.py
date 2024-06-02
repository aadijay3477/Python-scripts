import pyautogui
import time
import pygetwindow as gw
import keyboard
import random

# Constants for offsets and random variation
PIXEL_OFFSET = 5
TIME_VARIATION = 0.003
MAX_WAIT_TIME = 660  # 11 minutes in seconds
MIN_WAIT_TIME = 60  # 1 minute in seconds

IMAGE_PATH = {
    'archers': r'./Assets/Screen_20240602164210.png',
    'help-icon': r'./Assets/Screen_20240602022915.png',
    'down-key': r'./Assets/Screen_20240602023513.png',
    'troop-type': r'./Assets/Screen_20240602192343.png',
    'help-button': r'./Assets/Screen_20240602002218.png',
    'alliance-help': r'./Assets/Screen_20240602221430.png',
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
    random_sleep(0.2)
    pyautogui.keyDown('ctrl')
    random_sleep(0.189)
    pyautogui.press('a')
    random_sleep(0.376)
    pyautogui.keyUp('ctrl')
    random_sleep(0.2)
    pyautogui.press('backspace')
    random_sleep(0.26)
    pyautogui.press('7')
    random_sleep(0.207)
    pyautogui.press('0')
    random_sleep(0.199)
    pyautogui.press('0')
    random_sleep(0.39)

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

    while new_variable < 100:
        if keyboard.is_pressed('F8'):
            print("F8 pressed, stopping the macro.")
            break

        new_variable += 1
        random_sleep(0.103)  # Increased delay
        
        # Ensure the game window is activated before each interaction
        activate_window()
        
        # Perform clicks based on image paths
        if find_and_click_image('help-icon', 0.1):
            random_sleep(0.104)  # Increased delay
        
        activate_window()  # Ensure window is active before next interaction
        if find_and_click_image('down-key', 0.198):
            random_sleep(0.15)  # Increased delay
        
        activate_window()

        if find_and_click_image('troop-type', 0.18):
            random_sleep(0.17)
        activate_window()  # Ensure window is active before next interaction

        if find_and_click_image('help-button', 0.2):
            random_sleep(0.12)
        
        activate_window()  # Ensure window is active before next interaction
        if find_and_click_image('alliance-help', 0.2):
            random_sleep(0.14)
        
        activate_window()  # Ensure window is active before next interaction
        if find_and_click_image('archers', 0.33, max_wait=MAX_WAIT_TIME):
            print("Archers found and clicked.")

# Run the script
if __name__ == "__main__":
    activate_window()
    run_macro()