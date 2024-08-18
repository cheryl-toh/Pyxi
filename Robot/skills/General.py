from utils import factory
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from dataclasses import dataclass
import random

class General:

    def name(self, video_player:Animate, audio_player:Sound, pyxi:bool):
        video_player.play_animation("Happy")
        if pyxi:
            audio_player.play_sound("Name")
        else:
            audio_player.play_sound("Your Name")
        
    def mood(self, video_player:Animate, audio_player:Sound):
        mood = random.choice(["Happy", "Sad", "Angry"])
        video_player.play_animation(mood)
        audio_player.play_sound(mood)

    def encourage(self, video_player:Animate, audio_player:Sound):
        number = random.choice([1, 2, 3])
        random_encouragement = f"Encourage {number}"
        video_player.play_animation("Happy")
        audio_player.play_sound(random_encouragement)

    def sing(self, video_player:Animate, audio_player:Sound):
        number = random.choice([1, 2, 3, 4])
        random_song = f"Song {number}"
        video_player.play_animation("Sing")
        audio_player.play_sound(random_song)
        
    # def story(self, video_player:Animate, audio_player:Sound):
    #     return

class General_Skill:

    def __init__(self):
        self.skill_instance = General()

    def pyxi_name(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.name(video_player=video_player, audio_player=audio_player, pyxi=True)
    def your_name(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.name(video_player=video_player, audio_player=audio_player, pyxi=False)
    def mood(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.mood(video_player=video_player, audio_player=audio_player)
    def encourage(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.encourage(video_player=video_player, audio_player=audio_player)
    def sing(self, video_player:Animate, audio_player:Sound):
        self.skill_instance.sing(video_player=video_player, audio_player=audio_player)

@dataclass
class General_Handler():
    name = "general_handler"
    skill = General_Skill()

    def commands(self, command:str):
        return ["what's your name", "how are you", "who am i", "play by yourself", "go to sleep",
                "i am sad", r".* encouragement .*", r".* encouragement", r"encouragement .*",
                r".* sing .*", r".* sing", r"sing .*"]
    
    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        if command in ["what's your name"]:
            self.skill.pyxi_name(video_player=video_player, audio_player=audio_player)
        if command in ["who am i"]:
            self.skill.your_name(video_player=video_player, audio_player=audio_player)
        if command in ["how are you"]:
            self.skill.mood(video_player=video_player, audio_player=audio_player)
        if command in ["i am sad"] or "encouragement" in command:
            self.skill.encourage(video_player=video_player, audio_player=audio_player)
        if "sing" in command:
            self.skill.sing(video_player=video_player, audio_player=audio_player)
        
def initialize():
    factory.register('general_handler', General_Handler)
