import speech_recognition as sr
from .videoPlayer import Animate
from .audioPlayer import Sound

# Class for pyxi's speech recognition and responses
class Pyxi():
    name = ""
    skill = []

    def __init__(self, name=None, video_player=None, audio_player=None):
        self.r = sr.Recognizer()
        self.m = sr.Microphone(sample_rate=44100)
        self.video_player = video_player
        self.audio_player = audio_player
        self.keywords = ["pixie", "pictures", "bixby", "kitty", "hello"]
        if name is not None:
            self.name = name
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
        
    @property
    def name(self):
        return self.name
    
    @name.setter
    def name(self, value):
        self.name = value

    def wake_word(self):
        try: 
            print("Listening for wake word...")
            while True:
                with self.m as source:
                    self.r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.r.listen(source, 60, 2)
                    print("here")
                    text = self.r.recognize_google(audio)
                    print("herere")
                    print(text.lower())
                    if any(keyword in text.lower() for keyword in self.keywords):
                        print("Wake word detected.")
                        return True
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return False
                
        except sr.UnknownValueError:
            print("Unknown error occurred")
            return None

    def get_command(self):
        try:
            print("Say your command")
            with self.m as source:
                self.r.adjust_for_ambient_noise(source, duration=0.5)
                
                #listens for the user's input 
                audio = self.r.listen(source, 60, 4)
                self.video_player.play_animation("Loading")
                self.audio_player.play_sound("Loading")
                # Using google to recognize audio
                text = self.r.recognize_google(audio)
                self.audio_player.stop()
                text = text.lower()

            return text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return None
                
        except sr.UnknownValueError:
            print("unknown error occurred")
            self.audio_player.stop()
            return None
        

    def close_microphone(self):
        if self.m:
            try:
                self.m.__exit__(None, None, None)  # Manually exit the context to release the microphone
                print("Microphone closed successfully.")
            except Exception as e:
                print(f"Error closing microphone: {e}")
        else:
            print("Microphone was not initialized.")
