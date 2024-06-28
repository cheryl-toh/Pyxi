import socket
from dataclasses import dataclass
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from utils import factory

class Automate_Skill:
    def __init__(self):
        self.host = '192.168.1.27'  # Change: Windows machine IP
        self.port = 12345

    def send_command(self, command: str, audio_player:Sound):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((self.host, self.port))
                s.send(command.encode())
                audio_player.play_sound("Okay")
                print("Sending command:", command)

            self.close_connection()
        except Exception as e:
            print(f"Error sending command: {e}")

    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()
        print("close connection")

@dataclass
class Automate_Handler:
    name = "automate_handler"
    automate = Automate_Skill()

    def commands(self, command: str):
        return ["play me a song", r"^play .+$", r"^open .+$", "record my screen", "screen record", "take a screenshot", ]

    def handle_command(self, command: str, robot: Pyxi, video_player: Animate, audio_player:Sound, email:Email):
        if "play me a song" in command:
            self.automate.send_command("play me a song", audio_player)
        elif "play" in command:
            song_name = command.replace("play", "").strip()
            self.automate.send_command(f"play {song_name}", audio_player)
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            self.automate.send_command(f"open {app_name}", audio_player)
        elif "record my screen" in command:
            self.automate.send_command(f"record", audio_player)
        elif "screenshot" in command:
            self.automate.send_command(f"screenshot", audio_player)
        else:
            video_player.play_animation("Confused")
            audio_player.play_sound("Dont-understand")
            print("Unknown command")

def initialize():
    factory.register('automate_handler', Automate_Handler)
