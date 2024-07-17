import json
import os
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from utils import factory, loader
import contextlib
import re
import time

# Context manager to suppress ALSA warnings
@contextlib.contextmanager
def suppress_alsa_warnings():
    f = open(os.devnull, 'w')
    fd = os.dup(2)
    os.dup2(f.fileno(), 2)
    try:
        yield
    finally:
        os.dup2(fd, 2)
        f.close()
video_player = Animate()
audio_player = Sound()
email_sender = Email()
# Initialize objects
with suppress_alsa_warnings():
    robot = Pyxi(video_player=video_player, audio_player=audio_player)


# audio_player.play_sound("Name")
break_words = ["goodbye", "bye", "bye-bye", "go to sleep"]
command = ""

# Play initial loading screen
audio_player.play_sound("Start")
video_player.play_animation("Start")

file_path = os.path.join(os.path.dirname(__file__), 'utils', 'skills.json')

# load the skills
with open(file_path) as f:
    data = json.load(f)
    print("loading module", data)

    # load the plugins
    loader.load_skills(data["plugins"])

skills = [factory.create(item) for item in data["skills"]]
print(f'skills: {skills}')

audio_player.play_sound("Wake")

# main loop
while True and command not in ["good bye", 'bye', 'quit', 'exit', 'goodbye', 'exit']:
    video_player.play_animation("Neutral Static")
    command = ""
    with suppress_alsa_warnings():
        if robot.wake_word():
            audio_player.play_sound("Huh")
            video_player.play_animation("Listen")
            command = robot.get_command()
            if command:
                command = command.lower()
                handled = False
                print(f'command heard: {command}')
                if any(keyword in command for keyword in break_words):
                    break
                for skill in skills:
                    for pattern in skill.commands(command):
                        if re.match(pattern, command):
                            skill.handle_command(command, robot=robot, video_player=video_player, audio_player=audio_player, email=email_sender)
                            handled = True
                            break
                    if handled:
                        audio_player.play_sound("Wake")
                        break
                if not handled:
                    audio_player.play_sound("Dont-understand")
                    video_player.play_animation("Confused")
                    time.sleep(3)
            else:
                audio_player.play_sound("Dont-understand")
                video_player.play_animation("Confused")
                time.sleep(3)
                print('no command heard')

# sleep sound
audio_player.play_sound("Yawn")
video_player.play_animation("Sleep")
robot.close_microphone()
