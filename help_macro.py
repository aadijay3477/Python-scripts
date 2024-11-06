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
exit_flag = False  # Flag to exit the loop

print('Enter number of bots you are using:')
BOT_COUNT = int(input())

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

def activate_window(window):
    try:
        pywinauto.Application().connect(handle=window._hWnd).top_window().set_focus()
        random_sleep(0.155)
    except Exception as e:
        print(f"An error occurred while activating the window: {e}")

def run_macro():
    global exit_flag
    windows = gw.getWindowsWithTitle(ORIGINAL_TITLE)
    if len(windows) < BOT_COUNT:
        print("There are not enough windows with the specified title substring.")
        return

    while not exit_flag:
        for i in range(BOT_COUNT):
            if exit_flag:  # Exit immediately if flag is set
                break
            activate_window(windows[i])
            random_sleep(0.503)
            click(681, 669, 0.1)

# Function to listen for 'Q' key press in a separate thread
def listen_for_exit():
    global exit_flag
    keyboard.wait('q')  # Wait until 'q' is pressed
    exit_flag = True  # Set the flag to True to exit the loop
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
