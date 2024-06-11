
from utils.SpeechRecognition import Pyxi
from utils import factory, loader
import json

robot = Pyxi()

command = ""

# load the skills
with open("Robot\\utils\\skills.json") as f:
    data = json.load(f)
    print("loading module", data)

    # load the plugins
    loader.load_skills(data["plugins"])

skills = [factory.create(item) for item in data["skills"]]
print(f'skills: {skills}')
    

while True and command not in ["good bye", 'bye', 'quit', 'exit','goodbye', 'exit']:
    command = ""
    wake_word_detected = robot.wake_word()
    if wake_word_detected:
        command = robot.get_command()
        command = command.lower()
        print(f'command heard: {command}') 

        for skill in skills:
            if command in skill.commands(command):
                skill.handle_command(command, robot)