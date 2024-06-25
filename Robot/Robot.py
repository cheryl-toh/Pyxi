import json
import os
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from utils import factory, loader
import contextlib
import re

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

# Initialize objects
with suppress_alsa_warnings():
    robot = Pyxi()
video_player = Animate()
audio_player = Sound()
email_sender = Email()

# audio_player.play_sound("Name")

command = ""

# Play initial loading screen
# Add-on: can play loading sound
video_player.play_animation("Start")

# load the skills
with open("./utils/skills.json") as f:
    data = json.load(f)
    print("loading module", data)

    # load the plugins
    loader.load_skills(data["plugins"])

skills = [factory.create(item) for item in data["skills"]]
print(f'skills: {skills}')

# play robot face
audio_player.play_sound("Name") # Add-on: can change to wake up sound if want


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
                for skill in skills:
                    for pattern in skill.commands(command):
                        if re.match(pattern, command):
                            skill.handle_command(command, robot=robot, video_player=video_player, audio_player=audio_player, email=email_sender)
                            handled = True
                            break
                    if handled:
                        break
                if command in ["goodbye"]:
                    break
            else:
                # Add-on: sound saying "pyxi dont understand"
                # Add-on: video playing dont understand
                print('no command heard')

# sleep sound
video_player.play_animation("Sleep")
