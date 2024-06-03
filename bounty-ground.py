import pyautogui
import time
import pygetwindow as gw
import keyboard
import random

MAX_LIMIT_BOUNTY = 100
PIXEL_OFFSET = 5
TIME_VARIATION = 0.003

IMAGE_PATH = {
    'start-match': r'./Assets/Bounty/Screenshot220.png',
    'matching': r'./Assets/Bounty/Screenshot221.png',
    'final-screen': r'./Assets/Bounty/Screenshot222.png'
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
    top_margin = win.top + win.height // 4
    bottom_margin = win.top + 3 * win.height // 4
    left_margin = win.left + win.width // 4
    right_margin = win.left + 3 * win.width // 4

    target_x = random.randint(left_margin, right_margin)
    target_y = random.randint(top_margin, bottom_margin)

    offset_x = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
    offset_y = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)

    pyautogui.moveTo(center.x + offset_x, center.y + offset_y, duration)
    pyautogui.mouseDown()
    pyautogui.moveTo(target_x + offset_x, target_y + offset_y, duration)
    pyautogui.mouseUp()

def for_moving_army_randomly(center, duration):
    drag(center, duration)

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

def run_macro():
    new_variable = 0

    while new_variable < MAX_LIMIT_BOUNTY:
        if keyboard.is_pressed('F8'):
            print("F8 pressed, stopping the macro.")
            break

        new_variable += 1
        random_sleep(0.103)

        activate_window()
        random_sleep(0.2)

        if find_and_click_image('start-match', 0.1):
            random_sleep(0.104)

        activate_window()
        random_sleep(0.2)
        
        if find_and_click_image('matching', 0.15):
            random_sleep(0.15)

        activate_window()
        random_sleep(0.2)
        if find_and_click_image('final-screen', 0.17):
            random_sleep(0.17)

if __name__ == "__main__":
    activate_window()
    run_macro()