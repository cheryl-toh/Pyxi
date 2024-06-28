from datetime import datetime
import time
import threading
import pytz
import re
from countdowntimer import CountDownTimer
from utils import factory
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from dataclasses import dataclass

class Timer:
    def __init__(self):
        self.timer = CountDownTimer()
        self.timer_thread = None

    def countdown(self, video_player:Animate, audio_player:Sound):
        while not self.timer.isalarm():
            time.sleep(0.5)
        video_player.play_animation("Alarm")
        audio_player.play_sound("Alarm")
        time.sleep(4.5)

    def start_countdown(self, video_player:Animate, audio_player:Sound):
        self.timer.reset() 
        self.timer.duration_in_seconds = 10
        audio_player.play_sound("Okay")
        print("Countdown started, I'll let you know when it's done")
        self.timer_thread = threading.Thread(target=self.countdown, args=(video_player, audio_player,))
        self.timer_thread.start()

    def is_timer_active(self):
        return self.timer_thread and self.timer_thread.is_alive()

class Clock_Skill:

    def __init__(self):
        self.timer_instance = Timer()

    def local_time(self):
        local_time = datetime.now()
        local_timezone = pytz.timezone('Asia/Kuala_Lumpur')
        local_time = local_timezone.localize(local_time)
        return datetime.strftime(local_time,'%I:%M %p')
    
    def timer(self, video_player:Animate, audio_player:Sound):
        if self.timer_instance.is_timer_active():
            print("Timer is already running.")
            return
        self.timer_instance.start_countdown(video_player=video_player, audio_player=audio_player)

@dataclass
class Clock_Handler():
    name = "clock_handler"
    clock = Clock_Skill()

    def commands(self, command:str):
        return ["what's the time now", "tell me the time", "what time is it",
                r".* timer"]
    
    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        if command in ["what's the time now", "tell me the time", "what time is it"]:
            video_player.display_text(self.clock.local_time())
            audio_player.play_sound("ShowText")
            time.sleep(5)
        if "timer" in command:
            self.clock.timer(video_player=video_player, audio_player=audio_player)
def initialize():
    factory.register('clock_handler', Clock_Handler)
