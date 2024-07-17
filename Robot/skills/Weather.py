from pyowm.owm import OWM
from geopy import Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from datetime import datetime
import requests
from utils import factory
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from dataclasses import dataclass
import time


# Class for open weather api related functions
class Weather_Skill:

    # default location
    __location = "Kuala Lumpur, MY"

    # my API key
    apiKey = "e2ef6cc4a6b0b662298299dba098c702"

    def __init__(self):
        self.ow = OWM(self.apiKey)
        self.manager = self.ow.weather_manager()
        locator = Nominatim(user_agent="hi")
        self.city = "Kuala Lumpur"
        self.country = "MY"
        self.__location = f"{self.city}, {self.country}"
        self.lat = None
        self.long = None

        try:
            loc = locator.geocode(self.__location)
            if loc:
                self.lat = loc.latitude
                self.long = loc.longitude
            else:
                raise ValueError("Location not found")
        except GeocoderTimedOut:
            print("Geocoding service timed out")
        except GeocoderServiceError:
            print("Geocoding service error, insufficient privileges or other issue")
        except Exception as e:
            print(f"An unexpected error occurred during geocoding: {e}")

    @property
    def weather(self):
        if self.lat is None or self.long is None:
            print("Weather data could not be retrieved due to missing location data.")
            return None

        try:

            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.long}&units=imperial&APPID={self.apiKey}", verify=False)

            if weather_data.json()['cod'] == '404':
                print("No City Found")
            else:
                weather = weather_data.json()['weather'][0]['main']
            return weather
        except Exception as e:
            print(f"Error retrieving weather data: {e}")
            return None
        
    @property
    def temp(self):
        if self.lat is None or self.long is None:
            print("temp data could not be retrieved due to missing location data.")
            return None

        try:
            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.long}&units=imperial&APPID={self.apiKey}")

            if weather_data.json()['cod'] == '404':
                print("No City Found")
            else:
                temp = round(weather_data.json()['main']['temp'])
                c_temp = round(((temp-32)*5)/9, 1)
            return c_temp
        except Exception as e:
            print(f"Error retrieving weather data: {e}")
            return None

@dataclass
class Weather_Handler():
    name = "weather_handler"
    weather_skill = Weather_Skill()

    def commands(self, command:str):
        return [r".* weather .*", r"weather .*", r".* weather", "weather",
                r".* temperature .*", r".* temperature", r"temperature .*", "temperature"]
    
    def get_weather(self, video_player:Animate, audio_player=Sound):
        weather = self.weather_skill.weather
        if "clouds" in weather.lower():
            video_player.play_animation("Cloudy")
            audio_player.play_sound("Cloudy")
        elif "rain" in weather:
            video_player.play_animation("Rainy")
            audio_player.play_sound("Rainy")
        elif "thunder" in weather:
            video_player.play_animation("Thunder")
            audio_player.play_sound("Thunder")
        else:
            video_player.play_animation("Sunny")
            audio_player.play_sound("Sunny")
        time.sleep(5)
    
    def get_temp(self, video_player:Animate, audio_player=Sound):
        temp = str(self.weather_skill.temp) + "°C"
        audio_player.play_sound("Showtext")
        video_player.display_text(temp)
        time.sleep(5)

    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        
        if "weather" in command:
            self.get_weather(video_player=video_player, audio_player=audio_player)
        if "temperature" in command:
            self.get_temp(video_player=video_player, audio_player=audio_player)

def initialize():
    factory.register('weather_handler', Weather_Handler)
