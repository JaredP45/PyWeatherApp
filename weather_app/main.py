import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk

import requests
from dotenv import load_dotenv


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # App Window
        self.title("JPaubel Weather App")
        self.geometry("400x400")
        self.resizable(False, False)

        # Entry
        self.city_name = tk.StringVar()
        self.city_head = tk.Label(self, text='Enter City Name', font='Arial 12 bold').pack(pady=10)
        self.inp_city = tk.Entry(self, textvariable=self.city_name, width=24, font='Arial 14 bold').pack()

        # Process input, call API, and display information
        tk.Button(self, command=self.retrieve_weather, text="Check Weather",
                  font="Arial 10", bg='lightblue', fg='black',
                  activebackground="teal", padx=5, pady=5).pack(pady=20)

        self.weather_now = tk.Label(self, text="The Weather is:", font='arial 12 bold')
        self.tfield = tk.Text(self, width=46, height=10)
        self.tfield.pack()

    @staticmethod
    def time_format_for_location(utc_with_tz):
        local_time = datetime.utcfromtimestamp(utc_with_tz)
        return local_time.time()

    def retrieve_weather(self):
        load_dotenv()
        api_key = os.environ['API_KEY']

        weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + self.city_name.get() + '&appid=' + api_key
        response = requests.get(weather_url)
        weather_info = response.json()

        self.tfield.delete("1.0", "end")

        if weather_info['cod'] == 200:
            kelvin = 273
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

            weather = f"\nWeather of: {self.city_name.get()}\nTemperature (Celsius): " \
                      f"{temp}°\nFeels like in (Celsius): {feels_like_temp}°\nPressure: " \
                      f"{pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at " \
                      f"{sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
        else:
            weather = f"\n\tWeather for '{self.city_name.get()}' not found!\n\tKindly Enter valid City Name !!"

        self.tfield.insert(tk.INSERT, weather)


if __name__ == '__main__':
    app = WeatherApp()
    app.mainloop()
