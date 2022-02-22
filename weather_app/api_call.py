import os
from dotenv import load_dotenv
from datetime import datetime

import requests


class WeatherAPI:
    def __init__(self, utc_with_tz, city_name=''):
        self.utc_with_tz = utc_with_tz
        self.city_name = city_name

    def time_format_for_location(self, value):
        local_time = datetime.utcfromtimestamp(self.utc_with_tz)
        return local_time.time()

    def weather_api_call(self):
        load_dotenv()
        api_key = os.environ['API_KEY']

        weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + self.city_name + '&appid=' + api_key
        response = requests.get(weather_url)
        weather_info = response.json()

        return weather_info

    def retrieve_weather(self):
        weather_info = self.weather_api_call()

        if weather_info['cod'] == 200:
            kelvin = 273  # value of kelvin

            # -----------Storing the fetched values of weather of a city

            temp = int(weather_info['main']['temp'] - kelvin)  # converting default kelvin value to Celsius
            feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = weather_info['wind']['speed'] * 3.6
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']
            timezone = weather_info['timezone']
            cloudy = weather_info['clouds']['all']
            description = weather_info['weather'][0]['description']

            sunrise_time = self.time_format_for_location(sunrise + timezone)
            sunset_time = self.time_format_for_location(sunset + timezone)

            weather = f"\nWeather of: {self.city_name}\nTemperature (Celsius): " \
                      f"{temp}°\nFeels like in (Celsius): {feels_like_temp}°\nPressure: " \
                      f"{pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at " \
                      f"{sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
        else:
            weather = f"\n\tWeather for '{self.city_name}' not found!\n\tKindly Enter valid City Name !!"

        return weather
