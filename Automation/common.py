# COMMON CODE
import time
from pywinauto import Desktop, keyboard
import re

def find_window(title):
    windows = Desktop(backend="uia").windows()
    for win in windows:
        if re.search(re.escape(title), win.window_text(), re.IGNORECASE):
            return win
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



