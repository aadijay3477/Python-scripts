import sys
import pyautogui
import time
import keyboard
import random
import pygetwindow as gw
import pywinauto
import threading

# Constants for offsets and random variation
PIXEL_OFFSET = 3
TIME_VARIATION = 0.010
ORIGINAL_TITLE = 'Doomsday: Last Survivors'
exit_event = threading.Event()  # Thread-safe exit event

BOT_COUNT = 1  # For demo purposes; replace with user input if needed

# Image paths
IMAGE_PATH = {
    'attack': r'./Assets/zombie/attack_button.png',
    'stopped': r'./Assets/zombie/Stopped.png'
}

# Coordinates for 'stopped' image search area
STOPPED_SEARCH_AREA = (1312, 267, 1350, 291)

def find_and_click_image(image_key, duration, max_wait=10):
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

def find_stopped(max_wait=600):
    """Searches for the 'stopped' image within a specified region.
       Returns True if found within max_wait time, otherwise False.
    """
    image_path = IMAGE_PATH['stopped']
    print("Searching for 'stopped' image within specified area...")
    start_time = time.time()

    while True:
        try:
            location = pyautogui.locateOnScreen(image_path, region=STOPPED_SEARCH_AREA, confidence=0.8)
            if location:
                print(f"'Stopped' image found at {location}.")
                return True
        except pyautogui.ImageNotFoundException:
            print("Image not found within specified area.")
        except Exception as e:
            print(f"An error occurred: {e}")

        if (time.time() - start_time) > max_wait:
            print(f"'Stopped' image not found within the max wait time of {max_wait} seconds")
            return False
        random_sleep(1)

# Function to click at a specific position with a random offset
def click(x, y, duration=0.0):
    offset_x = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
    offset_y = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
    pyautogui.moveTo(x + offset_x, y + offset_y, duration)
    pyautogui.mouseDown()
    random_sleep(duration)
    pyautogui.mouseUp()

# Function to generate random sleep time with a small variation
def random_sleep(base_time):
    variation = random.uniform(-TIME_VARIATION * base_time, TIME_VARIATION * base_time)
    time.sleep(base_time + variation)

# Function to activate a specific window
def activate_window(window):
    try:
        pywinauto.Application().connect(handle=window._hWnd).top_window().set_focus()
        random_sleep(0.155)
    except Exception as e:
        print(f"An error occurred while activating the window: {e}")

# Main function to run the macro actions
def run_macro():
    counter = 0
    windows = gw.getWindowsWithTitle(ORIGINAL_TITLE)
    if len(windows) < BOT_COUNT:
        print("There are not enough windows with the specified title substring.")
        return

    while not exit_event.is_set() and counter < 67:
        for i in range(BOT_COUNT):
            if exit_event.is_set():  # Exit immediately if flag is set
                break
            activate_window(windows[i])
            random_sleep(1)
            click(43, 471, 0.1)    # Step: Search
            random_sleep(1.503)

            # Random clicks on + or - signs
            x = random.choice([386, 76])  # + or - sign coordinates
            num_clicks = random.randint(1,5)
            for _ in range(num_clicks):
                click(x, 416, 0.1)
                random_sleep(0.06)

            click(227, 497, 0.2)   # Step: Search button
            random_sleep(1.503)

            random_sleep(3.303)
            click(690, 376, 0.15)  # Step: Mid search button
            random_sleep(1.503)
            if find_and_click_image('attack', 0.5):
                random_sleep(1.503)
            else:
                continue
            click(1256, 731, 0.1)  # Step: Multiple check, one-time click per loop
            random_sleep(1.503)
            click(1028, 684, 0.1)  # Step: March button
            random_sleep(3)
            if find_stopped():
                print("'Stopped' detected. Proceeding to the next iteration.")
                pyautogui.hotkey('esc')
                random_sleep(0.100)
                pyautogui.hotkey('esc')
                random_sleep(0.489)
            else:
                print("Max wait time reached; proceeding without detecting 'Stopped'.")
        counter += 1

# Function to listen for 'Q' key press in a separate thread
def listen_for_exit():
    keyboard.wait('q')  # Wait until 'q' is pressed
    exit_event.set()  # Signal to exit the loop
    print("Exiting the macro...")

# Run the script
if __name__ == "__main__":
    # Start the exit listener thread
    exit_listener = threading.Thread(target=listen_for_exit)
    exit_listener.daemon = True  # Ensures the thread exits when the main program exits
    exit_listener.start()

    windows = gw.getWindowsWithTitle(ORIGINAL_TITLE)
    if windows:
        activate_window(windows[0])
        run_macro()
    else:
        print(f"No windows found with title: {ORIGINAL_TITLE}")
