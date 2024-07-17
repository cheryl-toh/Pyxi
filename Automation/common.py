# COMMON CODE
import time
from pywinauto import Desktop, keyboard
import re

def find_window(title, retries=2, delay=1):
    """ Find a window by title, with retries. """
    for _ in range(retries):
        windows = Desktop(backend="uia").windows()
        for win in windows:
            if re.search(re.escape(title), win.window_text(), re.IGNORECASE):
                print(f"Found window with title '{title}'")
                return win
        time.sleep(delay)
    return None

def start_app(title):
    keyboard.send_keys('{VK_LWIN}')

    time.sleep(1)

    # Type the name of the application in the search bar
    keyboard.send_keys(title)

    # Wait for a short time for the search results to appear
    time.sleep(1)

    # Press Enter to open the application
    keyboard.send_keys('{ENTER}')

    return True



