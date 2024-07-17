import socket
from dataclasses import dataclass
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from utils import factory

class Automate_Skill:
    def __init__(self):
        self.host = '192.168.211.208'  # Change: Windows machine IP
        self.port = 12345

    def send_command(self, command: str, video_player:Animate, audio_player:Sound):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                self.client_socket = s
                s.settimeout(1)
                s.connect((self.host, self.port))
                s.send(command.encode())
                audio_player.play_sound("Okay")
                print("Sending command:", command)

            self.close_connection()
        except Exception as e:
            video_player.display_text("Server Down")
            audio_player.play_sound("Error")
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
        return ["play me a song", r"^play .+$", r"^open .+$", "record my screen", "screen record", "take a screenshot",
        r".* shut down .*", r".* shut down", r"shut down .*",
        r".* sleep .*", r".* sleep", r"sleep .*",
        r".* restart .*", r".* restart", r"restart .*"]

    def handle_command(self, command: str, robot: Pyxi, video_player: Animate, audio_player:Sound, email:Email):
        if "play me a song" in command:
            self.automate.send_command("play me a song", video_player, audio_player)
        elif "play" in command:
            song_name = command.replace("play", "").strip()
            self.automate.send_command(f"play {song_name}", video_player, audio_player)
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            self.automate.send_command(f"open {app_name}", video_player, audio_player)
        elif "record my screen" in command:
            self.automate.send_command(f"record", video_player, audio_player)
        elif "screenshot" in command:
            self.automate.send_command(f"screenshot", video_player, audio_player)
        elif "shut down" in command:
            self.automate.send_command(f"shutdown", video_player, audio_player)
        elif "sleep" in command:
            self.automate.send_command(f"sleep", video_player, audio_player)
        elif "restart" in command:
            self.automate.send_command(f"restart", video_player, audio_player)
        else:
            video_player.play_animation("Confused")
            audio_player.play_sound("Dont-understand")
            print("Unknown command")

def initialize():
    factory.register('automate_handler', Automate_Handler)
