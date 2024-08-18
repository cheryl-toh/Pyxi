from datetime import datetime
import time
import threading
import pytz
import re
import os
from utils import factory
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from dataclasses import dataclass

class Easter:

    def birthday(self, video_player:Animate, audio_player:Sound):
        audio_player.play_sound("Birthday")
        video_player.play_animation("Birthday")
        
    def message(self, video_player:Animate, audio_player:Sound):
         sound_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Audio', 'Message.wav')
         if os.path.exists(sound_file_path):
            audio_player.play_sound("Message")
            video_player.play_animation("Read")
        
    def anniversary(self, video_player:Animate, audio_player:Sound):
        # Define the start date
        start_date = datetime(2023, 3, 12)
        
        # Get the current date
        current_date = datetime.now()
        
        # Calculate the difference between the current date and the start date
        difference = current_date - start_date
        
        # Calculate years, months, and days
        years = difference.days // 365
        remaining_days = difference.days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        
        # Return the formatted string
        countdown =  f"{years}Y {months}M {days}D"

        video_player.display_text(countdown)
        audio_player.play_sound("ShowText")
        time.sleep(4)
        


class Easter_Skill:

    def __init__(self):
        self.easter_instance = Easter()

    def birthday(self, video_player:Animate, audio_player:Sound):
        self.easter_instance.birthday(video_player=video_player, audio_player=audio_player)
    def message(self, video_player:Animate, audio_player:Sound):
        self.easter_instance.message(video_player=video_player, audio_player=audio_player)
    def anniversary(self, video_player:Animate, audio_player:Sound):
        self.easter_instance.anniversary(video_player=video_player, audio_player=audio_player)
    

@dataclass
class Easter_Handler():
    name = "easter_handler"
    skill = Easter_Skill()

    def commands(self, command:str):
        return ["it's my birthday", "secret message", "how long have we been together"]
    
    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        if command in ["it's my birthday"]:
            self.skill.birthday(video_player=video_player, audio_player=audio_player)
        if command in ["secret message"]:
            self.skill.message(video_player=video_player, audio_player=audio_player)
        if command in ["how long have we been together"]:
            self.skill.anniversary(video_player=video_player, audio_player=audio_player)
       
def initialize():
    factory.register('easter_handler', Easter_Handler)
