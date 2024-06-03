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

# Activate the game window
def activate_window():
    try:
        win = gw.getWindowsWithTitle('Doomsday: Last Survivors')[0]
        win.activate()
        random_sleep(0.533)  # Adjusted for the initial sleeps
    except IndexError:
        print("Window not found!")

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

def wait_for_image(image_key, confidence=0.8, timeout=30):
    image_path = IMAGE_PATH[image_key]
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location is not None:
                print(f"Detected image: {image_key}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(1)
    return False

def run_macro():
    new_variable = 0

    while new_variable < MAX_LIMIT_BOUNTY:
        if keyboard.is_pressed('F8'):
            print("F8 pressed, stopping the macro.")
            break

        new_variable += 1
        random_sleep(0.103)  # Increased delay

        # Ensure the game window is activated before each interaction
        activate_window()

        # Perform clicks based on image paths (examples)
        if find_and_click_image('start-match', 0.1):
            random_sleep(0.104)  # Increased delay

        activate_window()  # Ensure window is active before next interaction
        if find_and_click_image('matching', 0.15):
            random_sleep(0.15)  # Increased delay

        activate_window()
        if find_and_click_image('final-screen', 0.17):
            random_sleep(0.17)

# Initial actions before running the macro
if find_and_click_image('start-match', 0.1):
    print("Clicked 'Match' button.")
else:
    print("Failed to find 'Match' button.")
    exit()

if wait_for_image('matching', confidence=0.8, timeout=30):
    print("Detected 'Matching...' screen.")
else:
    print("Failed to detect 'Matching...' screen.")
    exit()

if wait_for_image('final-screen', confidence=0.8, timeout=30):
    print("Detected final game screen.")
else:
    print("Failed to detect final game screen.")
    exit()

print("Waiting for 18 seconds.")
time.sleep(18)
print("18 seconds wait completed.")

if __name__ == "__main__":
    activate_window()
    run_macro()