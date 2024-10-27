import pyautogui
import time
import pygetwindow as gw
import keyboard
import random

MAX_LIMIT_BOUNTY = 2000
PIXEL_OFFSET = 5
TIME_VARIATION = 0.003
DRAG_INTERVAL = 5  # Time in seconds between drag operations

IMAGE_PATH = {
    'start-match': r'./Assets/Bounty/Screenshot220.png',
    'matching': r'./Assets/Bounty/Screenshot221.png',
    'final-screen': r'./Assets/Bounty/Screenshot222.png',
    'exit': r'./Assets/Bounty/exit.png',
    'try-again': r'./Assets/Bounty/Tryagain.png',
}

def random_sleep(base_time):
    variation = random.uniform(-TIME_VARIATION * base_time, TIME_VARIATION * base_time)
    time.sleep(base_time + variation)

def click(x, y, duration=0.0):
    offset_x = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
    offset_y = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
    pyautogui.moveTo(x + offset_x, y + offset_y, duration)
    pyautogui.mouseDown()
    time.sleep(duration)
    pyautogui.mouseUp()

def drag(center, duration):
    win = gw.getWindowsWithTitle('Doomsday: Last Survivors')[0]
    top_margin = win.top + win.height // 3
    bottom_margin = win.top + 2 * win.height // 3
    left_margin = win.left + win.width // 3
    right_margin = win.left + 2 * win.width // 3

    target_x = random.randint(left_margin, right_margin)
    target_y = random.randint(top_margin, bottom_margin)

    offset_x = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
    offset_y = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)

    pyautogui.moveTo(center.x + offset_x, center.y + offset_y, duration)
    pyautogui.mouseDown()
    time.sleep(3)
    pyautogui.moveTo(target_x + offset_x, target_y + offset_y, duration)
    pyautogui.mouseUp()

def for_moving_army_randomly(center, duration):
    last_drag_time = time.time() - DRAG_INTERVAL
    while True:
        current_time = time.time()
        if current_time - last_drag_time >= DRAG_INTERVAL:
            drag(center, duration)
            last_drag_time = current_time  # Update last_drag_time after successful drag
        # Check if 'exit' button appears during drag
        if pyautogui.locateOnScreen(IMAGE_PATH['exit'], confidence=0.6) is not None:
            print("Exit button detected during drag. Stopping drag operation.")
            break

def find_and_click_image(image_key, duration, max_wait=10):
    image_path = IMAGE_PATH[image_key]
    print(f"Looking for image: {image_key}")
    # if image_key == 'final-screen': 
    #     max_wait = 240
    start_time = time.time()

    while True:
        for confidence_threshold in range(10, 4, -1):
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=(confidence_threshold / 10.0))
                if location is not None:
                    center = pyautogui.center(location)
                    print(f"Image found at: {location}, center at: {center}, confidence: {(confidence_threshold / 10.0)}")
                    if image_key == 'final-screen':
                        for_moving_army_randomly(center, duration)
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

def activate_window():
    try:
        win = gw.getWindowsWithTitle('Doomsday: Last Survivors')[0]
        if not win.isActive:
            print("Activating window...")
            win.activate()
            random_sleep(0.533)
            if win.isActive:
                print("Window activated successfully.")
            else:
                print("Failed to activate window.")
        else:
            print("Window already active.")
    except IndexError:
        print("Window not found!")

def process_step(image_key, click_duration):
    activate_window()
    random_sleep(0.2)
    return find_and_click_image(image_key, click_duration)

def run_macro():
    new_variable = 0

    while new_variable < MAX_LIMIT_BOUNTY:
        if keyboard.is_pressed('F8'):
            print("F8 pressed, stopping the macro.")
            break

        new_variable += 1
        random_sleep(0.103)

        if process_step('start-match', 0.1):
            random_sleep(0.104)
        if process_step('matching', 0.15):
            random_sleep(0.15)
        if process_step('final-screen', 0.17):
            random_sleep(0.17)
        if process_step('exit', 0.17):
            random_sleep(0.17)
        if process_step('try-again', 0.17):
            random_sleep(0.17)

if __name__ == "__main__":
    activate_window()
    run_macro()