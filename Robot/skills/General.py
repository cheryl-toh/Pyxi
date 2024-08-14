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

class General:
    # def __init__(self):
    #     self.timer = CountDownTimer()
    #     self.timer_thread = None

    def name(self, video_player:Animate, audio_player:Sound):
        
    def mood(self, video_player:Animate, audio_player:Sound):
    
    def play(self, video_player:Animate, audio_player:Sound):

    def sing(self, video_player:Animate, audio_player:Sound):
    
    def story(self, video_player:Animate, audio_player:Sound):


class General_Skill:

    def __init__(self):
        self.skill_instance = General()

    def pyxi_name(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.name(video_player=video_player, audio_player=audio_player)
    def your_name(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.name(video_player=video_player, audio_player=audio_player)
    def mood(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.mood(video_player=video_player, audio_player=audio_player)
    def play(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.play(video_player=video_player, audio_player=audio_player)
    def sing(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.sing(video_player=video_player, audio_player=audio_player)

@dataclass
class General_Handler():
    name = "general_handler"
    skill = General_Skill()

    def commands(self, command:str):
        return ["what's your name", "how are you", "who am I", "play by yourself", "go to sleep",
                r".* favourite food .*", r".* favourite food", r"favourite food .*", 
                r".* favourite music .*", r".* favourite music", r"favourite music .*", 
                r".* sing .*", r".* sing", r"sing .*"]
    
    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        if command in ["what's your name"]:
            self.skill.pyxi_name(video_player=video_player, audio_player=audio_player)
        if command in ["who am I"]:
            self.skill.your_name(video_player=video_player, audio_player=audio_player)
        if command in ["how are you"]:
            self.skill.mood(video_player=video_player, audio_player=audio_player)
        if command in ["play by yourself"]:
            self.skill.play(video_player=video_player, audio_player=audio_player)
        if "sing" in command:
            self.skill.sing(video_player=video_player, audio_player=audio_player)
def initialize():
    factory.register('general_handler', General_Handler)
