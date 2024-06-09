from pyowm.owm import OWM
from geopy import Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from datetime import datetime
import requests


# Class for open weather api related functions
class OpenWeatherApi:

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
                print(loc.latitude)
                self.long = loc.longitude
                print(loc.longitude)
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
                f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.long}&units=imperial&APPID={self.apiKey}")

            if weather_data.json()['cod'] == '404':
                print("No City Found")
            else:
                weather = weather_data.json()['weather'][0]['main']

                print(f"The weather in {self.city} is: {weather}")
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
            return temp
        except Exception as e:
            print(f"Error retrieving weather data: {e}")
            return None

# myweather = Weather()
# weather_data = myweather.weather

# if weather_data:
#     print(weather_data)
# else:
#     print("Weather data could not be retrieved.")
