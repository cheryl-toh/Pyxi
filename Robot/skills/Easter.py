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

class Easter:
    # def __init__(self):
    #     self.timer = CountDownTimer()
    #     self.timer_thread = None

    def birthday(self, video_player:Animate, audio_player:Sound):
        
    def message(self, video_player:Animate, audio_player:Sound):
    
    def anniversary(self, video_player:Animate, audio_player:Sound):

    # def sing(self, video_player:Animate, audio_player:Sound):
    
    # def story(self, video_player:Animate, audio_player:Sound):


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
        return ["it's my birthday", "any message from boss", "anniversary reminder"]
    
    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        if command in ["it's my birthday"]:
            self.skill.birthday(video_player=video_player, audio_player=audio_player)
        if command in ["any message from boss"]:
            self.skill.message(video_player=video_player, audio_player=audio_player)
        if command in ["anniversary reminder"]:
            self.skill.anniversary(video_player=video_player, audio_player=audio_player)
       
def initialize():
    factory.register('easter_handler', Easter_Handler)
