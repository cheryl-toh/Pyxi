from datetime import datetime
import time
import threading
import pytz
from countdowntimer import CountDownTimer
from utils import factory
from utils.SpeechRecognition import Pyxi
from dataclasses import dataclass

class Timer:
    def __init__(self):
        self.timer = CountDownTimer()

    def countdown(self):
        while not self.timer.isalarm():
            time.sleep(0.5)
        print("Times up!")

    def start(self):
        self.timer.reset()  # Use self.timer.reset() instead of self.timer.reset()
        self.timer.duration_in_seconds = 10
        print("Countdown started, I'll let you know when it's done")
        thread = threading.Thread(target=self.countdown)
        thread.start()

class Clock_Skill:

    def local_time(self):
        local_time = datetime.now()
        local_timezone = pytz.timezone('Asia/Kuala_Lumpur')  # Replace with your local time zone
        local_time = local_timezone.localize(local_time)
        return datetime.strftime(local_time,'%H:%M:%S')
    
    def timer(self):
        timer = Timer()
        timer.start()

@dataclass
class Clock_Handler():
    name = "clock_handler"
    clock = Clock_Skill()

    def commands(self, command:str):
        return ["what's the time now", "tell me the time", "what time is it",
                "start a timer"]
    
    def handle_command(self, command:str, robot:Pyxi):
        if command in ["what's the time now", "tell me the time", "what time is it"]:
            print(self.clock.local_time())
        if command in ["start a timer"]:
            self.clock.timer()

def initialize():
    factory.register('clock_handler', Clock_Handler)
