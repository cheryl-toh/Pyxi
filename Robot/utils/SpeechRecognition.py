import speech_recognition as sr
import pvporcupine
import pyaudio
import struct
from .videoPlayer import Animate
from .audioPlayer import Sound
import os

# Class for pyxi's speech recognition and responses
class Pyxi():
    name = ""
    skill = []

    def __init__(self, name=None, video_player=None, audio_player=None):
        self.r = sr.Recognizer()
        self.m = sr.Microphone(sample_rate=44100)
        self.video_player = video_player
        self.audio_player = audio_player
        self.wake_word_path =  os.path.join(os.path.dirname(__file__), "wakeword.ppn")
        self.porcupine = pvporcupine.create(access_key="xaXfRKmlPbzR5pqcLKM2rchbUOlfaba2+QS/Vjl4jGW/v66ZiaNOrA==", keyword_paths=[self.wake_word_path])
        self.audio_stream = None
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
            self.audio_stream = pyaudio.PyAudio().open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            print("Listening for wake word...")
            try:
                while True:
                    pcm = self.audio_stream.read(self.porcupine.frame_length)
                    pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                    keyword_index = self.porcupine.process(pcm)
                    if keyword_index >= 0:
                        print("Wake word detected.")
                        return True
            except KeyboardInterrupt:
                print("Stopping...")
            finally:
                if self.audio_stream is not None:
                    self.audio_stream.close()

    def get_command(self):
        try:
            print("Say your command")
            with self.m as source:
                self.r.adjust_for_ambient_noise(source, duration=1)
                
                #listens for the user's input 
                audio = self.r.listen(source, 60, 4)
                self.video_player.play_animation("Loading")
                self.audio_player.play_sound("Loading")
                # Using google to recognize audio
                print("here")
                text = self.r.recognize_google(audio)
                print("herere")
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

        if self.audio_stream is not None:
            self.audio_stream.close()
        self.porcupine.delete()
