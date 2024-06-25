
import time
from . import common


def open_and_play():
    try:

        spotify_window = common.find_window("Spotify")

        if not spotify_window:
            # Start Spotify application
            common.start_app("Spotify")

            # Wait for Spotify to open
            time.sleep(7)

            spotify_window = common.find_window("Spotify")

        if spotify_window:
            spotify_window.set_focus()
            print("Spotify window found and focused.")
            time.sleep(1)
            spotify_window.type_keys("{VK_SPACE}")  # Press space bar to play/pause
            print("Space bar pressed.")

        else:
            print("Spotify window not found.")

    except Exception as e:
        print(f"Error finding or focusing Spotify window: {e}")
    
    return True


# Code for opening spotify and searching a song to play  
def search_and_play(keyword):

    try:
        spotify_window = common.find_window("Spotify")

        if not spotify_window:
            # Start Spotify application
            common.start_app("Spotify")

            # Wait for Spotify to open
            time.sleep(7)

            spotify_window = common.find_window("Spotify")

        if spotify_window:
            spotify_window.set_focus()
            print("Spotify window found and focused.") 
            time.sleep(1)
        # Focus the search bar
            spotify_window.type_keys("^l")  # Ctrl + L to focus the search bar
            time.sleep(1)

            # Type the song name and press Enter
            spotify_window.type_keys(keyword) 
            spotify_window.type_keys("{ENTER}")
            print(f"Searching for '{keyword}'")

            # Wait for results to load and press Enter again to play the first result
            time.sleep(2.5)
            # Navigate to the first result
            spotify_window.type_keys("{ENTER}")
            spotify_window.type_keys("{TAB}")
            spotify_window.type_keys("{ENTER}")
            time.sleep(2.5)
            spotify_window.type_keys("{TAB}")
            spotify_window.type_keys("{ENTER}")
            print("Playing the first search result.")
            return True
        else:
            print("Spotify window not found.")
            return True

    except Exception as e:
        print(f"Error finding or focusing Spotify window: {e}")
    
        return True