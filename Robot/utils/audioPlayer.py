import pygame
import time
import os
import threading

class Sound():

    def __init__(self):
        pygame.mixer.init()
        self.sound_thread = None
        self.sound_stop_event = threading.Event()

    def play_sound(self, file_name:str):
        if self.sound_thread and self.sound_thread.is_alive():
            self.sound_stop_event.set()  # Set stop event to terminate current animation thread
            self.sound_thread.join()

        # Start a new animation thread
        self.sound_stop_event.clear()
        self.sound_thread = threading.Thread(target=self._sound_worker, args=(file_name,))
        self.sound_thread.start()

    def _sound_worker(self, file_name:str):
        file_path =  os.path.join(os.path.dirname(__file__), '..','..', 'Audio', f"{file_name}.wav")

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def stop(self):
        pygame.mixer.music.stop()

    def quit(self):
        pygame.mixer.quit()
