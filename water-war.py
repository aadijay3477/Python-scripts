import pyautogui
import time
import pygetwindow as gw
import keyboard
import random

MAX_LIMIT_BOUNTY = 10  # Set to 10 for initial testing
PIXEL_OFFSET = 5
TIME_VARIATION = 0.003
DRAG_INTERVAL = 5  # Time in seconds between drag operations

IMAGE_PATH = {
    'Match': r'./Assets/waterwar/Match.png',
    'Ready': r'./Assets/waterwar/Ready.png',
    'Building_Right': r'./Assets/waterwar/Building_Right.png',
    'Building_Left': r'./Assets/waterwar/Building_Left.png',
    'March': r'./Assets/waterwar/March.png',
    'Exit': r'./Assets/waterwar/Exit.png',
    'Fighting': r'./Assets/waterwar/Fighting.png',
    'Name': r'./Assets/waterwar/Name.png',
    'Picked_water': r'./Assets/waterwar/Picked_water.png',
    'Tap_empty': r'./Assets/waterwar/Tap_empty.png',
    'Zombie': r'./Assets/waterwar/Zombie.png',
    'Sprinting': r'./Assets/waterwar/Sprinting.png',
    'Return': r'./Assets/waterwar/Return.png',
    'Profile': r'./Assets/waterwar/Profile.png',
    'Pickup': r'./Assets/waterwar/Pickup.png',
    'Home': r'./Assets/waterwar/Home.png',
    'All_checked': r'./Assets/waterwar/checked.png',
    'All_unchecked': r'./Assets/waterwar/unchecked.png',
    'zombie_boss': r'./Assets/waterwar/zombie_boss.png',
    'zombie_boss_icon': r'./Assets/waterwar/zombie_boss_icon.png',
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

def drag(center, duration, direction):
    try:
        win = gw.getWindowsWithTitle('Doomsday: Last Survivors')[0]
        top_margin = win.top + win.height // 3
        bottom_margin = win.top + 2 * win.height // 3
        left_margin = win.left + win.width // 3
        right_margin = win.left + 2 * win.width // 3

        if direction == 'left':
            target_x = random.randint(left_margin, center.x - 50)
        else:
            target_x = random.randint(center.x + 50, right_margin)
        target_y = random.randint(bottom_margin, win.bottom - 10)

        offset_x = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)
        offset_y = random.randint(-PIXEL_OFFSET, PIXEL_OFFSET)

        pyautogui.moveTo(center.x + offset_x, center.y + offset_y, duration)
        pyautogui.mouseDown()
        time.sleep(1)
        pyautogui.moveTo(target_x + offset_x, target_y + offset_y, duration)
        pyautogui.mouseUp()
    except Exception as e:
        print(f"Error during drag operation: {e}")

def for_moving_army_randomly(center, duration):
    last_drag_time = time.time() - DRAG_INTERVAL
    while True:
        current_time = time.time()
        if current_time - last_drag_time >= DRAG_INTERVAL:
            drag(center, duration, random.choice(['left', 'right']))
            last_drag_time = current_time  # Update last_drag_time after successful drag
        # Check if 'exit' button appears during drag
        if pyautogui.locateOnScreen(IMAGE_PATH['Exit'], confidence=0.6) is not None:
            print("Exit button detected during drag. Stopping drag operation.")
            break

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

def handle_zombies():
    while True:
        if pyautogui.locateOnScreen(IMAGE_PATH['All_unchecked'], confidence=0.6) is not None:
            find_and_click_image('All_unchecked', 0.1)
            random_sleep(0.1)
            find_and_click_image('All_checked', 0.1)
        if find_and_click_image('Zombie', 0.1):
            random_sleep(0.1)
            if find_and_click_image('Fighting', 0.1):
                random_sleep(0.1)
                if find_and_click_image('Pickup', 0.1):
                    random_sleep(0.1)
                    find_and_click_image('Picked_water', 0.1)
                    return
        random_sleep(0.1)

def run_macro():
    for i in range(MAX_LIMIT_BOUNTY):
        if keyboard.is_pressed('F8'):
            print("F8 pressed, stopping the macro.")
            break

        if process_step('Match', 0.1):
            random_sleep(10)  # Wait for match to proceed

        while not process_step('Ready', 0.1):
            random_sleep(5)  # Check for ready button every 5 seconds

        if process_step('Ready', 0.1):
            random_sleep(10)  # Wait for match to start

        building_found = False
        while not building_found:
            right_building_location = pyautogui.locateOnScreen(IMAGE_PATH['Building_Right'], confidence=0.6)
            left_building_location = pyautogui.locateOnScreen(IMAGE_PATH['Building_Left'], confidence=0.6)
            if right_building_location:
                drag(pyautogui.center(right_building_location), 0.2, 'right')
                building_found = True
            elif left_building_location:
                drag(pyautogui.center(left_building_location), 0.2, 'left')
                building_found = True
            random_sleep(2)  # Check for building every 2 seconds

        handle_zombies()

        if process_step('Return', 0.1):
            random_sleep(30)  # Wait for return process
            if pyautogui.locateOnScreen(IMAGE_PATH['Profile'], confidence=0.6) is not None:
                random_sleep(20)
                continue  # Retry from step 3 if failed

        while not find_and_click_image('zombie_boss_icon', 0.1):
            random_sleep(15)  # Wait for zombie boss icon every 15 seconds

        random_sleep(14)
        zombie_boss_center = pyautogui.locateCenterOnScreen(IMAGE_PATH['zombie_boss_icon'], confidence=0.6)
        if zombie_boss_center:
            for_moving_army_randomly(zombie_boss_center, 0.2)

        if find_and_click_image('Tap_empty', 0.1):
            random_sleep(2)
            find_and_click_image('Exit', 0.1)

if __name__ == "__main__":
    activate_window()
    run_macro()
