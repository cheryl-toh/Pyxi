from pywinauto import keyboard
import pyautogui
import time

# Code for taking screenshot - 3

def screenshot():
    # Press Win+Shift+S to open the snipping tool
    keyboard.send_keys('{VK_LWIN down}{VK_SHIFT down}s{VK_LWIN up}{VK_SHIFT up}')
    time.sleep(1)  # Wait for the snipping tool to open

    keyboard.send_keys('{ENTER}')
    time.sleep(1)

    # Get the current mouse position using pyautogui
    x, y = pyautogui.position()

    # Simulate a mouse click at the current mouse position
    pyautogui.click(x,y)

    return True



# Code for starting/stopping screen record - 2
def screen_record():
    # Press Win+Shift+S to open the xbox play bar tool
    keyboard.send_keys('{VK_LWIN down}g{VK_LWIN up}')

    time.sleep(1)  # Wait for the xbox tool to open

    #  start recording
    keyboard.send_keys('{VK_LWIN down}{VK_MENU down}r{VK_LWIN up}{VK_MENU up}')
    
    return True


# code for turning off or sleeping laptop - 5
def laptop(action:str):
    keyboard.send_keys('{VK_LWIN down}x{VK_LWIN up}')
    time.sleep(0.5)

    if action == "shutdown":
        keyboard.send_keys('{UP}{UP}{ENTER}{DOWN}{DOWN}{ENTER}')
    elif action == "sleep":
        keyboard.send_keys('{UP}{UP}{ENTER}{DOWN}{ENTER}')
    elif action == "restart":
        keyboard.send_keys('{UP}{UP}{ENTER}{DOWN}{DOWN}{DOWN}{ENTER}')

    return True