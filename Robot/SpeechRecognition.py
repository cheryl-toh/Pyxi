import speech_recognition as sr

# Class for pyxi's speech recognition and responses
class Pyxi():
    name = ""
    skill = []

    def __init__(self, name=None):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()

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

    def say(self, sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()

    def wake_word(self):
        try: 
            print("Listening for wake word...")
            while True:
                with self.m as source:
                    self.r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.r.listen(source)
                    text = self.r.recognize_google(audio)
                    if text.lower() in ["pyxi", "pixie"]:
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
                self.r.adjust_for_ambient_noise(source, duration=0.2)
                
                #listens for the user's input 
                audio = self.r.listen(source)
                    
                # Using google to recognize audio
                text = self.r.recognize_google(audio)
                text = text.lower()

            return text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return None
                
        except sr.UnknownValueError:
            print("unknown error occurred")
            return None
        

    