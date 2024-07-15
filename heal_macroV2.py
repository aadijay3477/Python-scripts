import pyautogui
import time
import keyboard
import random
import pygetwindow as gw
import pywinauto

# Constants for offsets and random variation
PIXEL_OFFSET = 3
TIME_VARIATION = 0.003
MAX_LIMIT_HEAL = 300
MAX_WAIT_TIME = 26 * 60  # 26 minutes in seconds
MIN_WAIT_TIME = 60  # 1 minute in seconds
ORIGINAL_TITLE = 'Doomsday: Last Survivors'

IMAGE_PATH = {
    'archers': r'./Assets/Heal/rider_collect.png',    
    'help-icon': r'./Assets/Heal/Screen_20240602022915.png',
    'down-key': r'./Assets/Heal/Screen_20240602023513.png',
    'troop-type': r'./Assets/Heal/rider_heal.png',  
    'help-button': r'./Assets/Heal/Screen_20240602002218.png',
    'alliance-help': r'./Assets/Heal/Screen_20240602221430.png',
    'help_provide': r'./Assets/Heal/help_provide.png'  
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
    click(center.x + 390, center.y + 11, duration)  
    random_sleep(0.2)
    pyautogui.keyDown('ctrl')
    random_sleep(0.189)
    pyautogui.press('a')
    random_sleep(0.376)
    pyautogui.keyUp('ctrl')
    random_sleep(0.2)
    pyautogui.press('backspace')
    random_sleep(0.26)
    pyautogui.press('2')
    random_sleep(0.207)
    pyautogui.press('3')
    random_sleep(0.199)
    pyautogui.press('0')
    random_sleep(0.39)

# Function to find and click the image
def find_and_click_image(image_key, duration, max_wait=0):
    image_path = IMAGE_PATH[image_key]
    print(f"Looking for image: {image_key}")  
    start_time = time.time()

    while True:
        for confidence_threshold in range(10, 3, -1):
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=(confidence_threshold / 10.0))
                if location is not None:
                    center = pyautogui.center(location)
                    print(f"Image found at: {location}, center at: {center}, confidence: {(confidence_threshold / 10.0)}")
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
        random_sleep(1)

# Activate a specific window by its handle
def activate_window(window):
    try:
        pywinauto.Application().connect(handle=window._hWnd).top_window().set_focus()
        random_sleep(0.533)
    except Exception as e:
        print(f"An error occurred while activating the window: {e}")

# Main function to run the macro
def run_macro():
    windows = gw.getWindowsWithTitle(ORIGINAL_TITLE)
    if len(windows) < 3:
        print("There are not enough windows with the specified title substring.")
        return

    original_window = windows[0]
    secondary_window_1 = windows[1]
    secondary_window_2 = windows[2]

    new_variable = 0

    while new_variable < MAX_LIMIT_HEAL:
        if keyboard.is_pressed('F8'):
            print("F8 pressed, stopping the macro.")
            break

        new_variable += 1
        random_sleep(0.103)  
        
        activate_window(original_window)
        
        if find_and_click_image('help-icon', 0.1):
            random_sleep(0.104)  
        
        activate_window(original_window)  
        if find_and_click_image('down-key', 0.198):
            random_sleep(0.15)  
        
        activate_window(original_window)

        if find_and_click_image('troop-type', 0.18):
            random_sleep(0.17)
        
        activate_window(original_window)  

        if find_and_click_image('help-button', 0.2):
            random_sleep(0.12)
        
        activate_window(original_window)  
        if find_and_click_image('alliance-help', 0.2):
            random_sleep(0.14)
        
        activate_window(secondary_window_1)
        if find_and_click_image('help_provide', 0.2):
            random_sleep(0.13)
        
        activate_window(secondary_window_2)
        if find_and_click_image('help_provide', 0.2):
            random_sleep(0.13)
        
        activate_window(original_window) # Ensure the original window is active
        if find_and_click_image('archers', 0.33, max_wait=MAX_WAIT_TIME):
            print("Archers found and clicked.")

# Run the script
if __name__ == "__main__":
    windows = gw.getWindowsWithTitle(ORIGINAL_TITLE)
    if windows:
        activate_window(windows[0])
        run_macro()
    else:
        print(f"No windows found with title: {ORIGINAL_TITLE}")
