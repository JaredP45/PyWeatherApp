import os
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk

import requests
from dotenv import load_dotenv


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Weather Wizard")
        self.geometry("450x450")
        self.resizable(False, False)

        # Title
        self.city_head = tk.Label(self, text='Weather Wizard', font='Arial 18 bold')
        self.city_head.grid(column=0, row=0)

        # City Name Entry
        self.city_name = tk.StringVar()

        self.city = tk.Label(self, text='Enter City Name', font='Arial 12')
        self.city.grid(column=0, row=1, sticky=tk.W, padx=10)

        self.input_city = tk.Entry(self, textvariable=self.city_name, width=16, font='Arial 12')
        self.input_city.grid(column=0, row=2, sticky=tk.W, padx=10)

        # Zip Code Entry
        self.zip_code = tk.StringVar()

        self.zip = tk.Label(self, text='Enter Zip Code', font='Arial 12')
        self.zip.grid(column=0, row=1, sticky=tk.E, padx=10)

        self.input_zip = tk.Entry(self, textvariable=self.zip_code, width=16, font='Arial 12')
        self.input_zip.grid(column=0, row=2, sticky=tk.E, padx=10)

        # Process input, call API, and display information
        tk.Button(self, command=self.RetrieveWeather, text="Check Weather",
                  font="Arial 10", bg='lightblue', fg='black',
                  activebackground="teal", padx=25, pady=5).grid(row=3, pady=10)

        self.weather_now = tk.Label(self, text="The Weather is: ", font='arial 12')
        self.weather_now.grid(row=4)

        self.weather_response = tk.Text(self, width=40, height=12)
        self.weather_response.grid(row=5, padx=20)
        self.weather_response.config(state='disabled')

    def ClearText(self):
        self.input_zip.delete(0, END)
        self.input_city.delete(0, END)

    @staticmethod
    def C_to_F(temp):
        return (temp * 1.80) + 32.00

    @staticmethod
    def time_format_for_location(utc_with_tz):
        local_time = datetime.utcfromtimestamp(utc_with_tz)
        return local_time.time()

    def RetrieveWeather(self):
        load_dotenv()
        api_key = os.environ['API_KEY']

        self.weather_response.config(state='normal')
        self.weather_response.delete("1.0", "end")

        if len(self.city_name.get()) != 0:
            search_option = self.city_name.get().capitalize()
            weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + self.city_name.get() + '&appid=' + api_key
            weather_info = requests.get(weather_url).json()
        else:
            search_option = self.zip_code.get()
            weather_url = 'http://api.openweathermap.org/data/2.5/weather?zip=' + self.zip_code.get() + '&appid=' + api_key
            weather_info = requests.get(weather_url).json()

        if weather_info['cod'] == 200:
            kelvin = 273
            temp = int(weather_info['main']['temp'] - kelvin)   # Convert from kelvin to Celsius
            feels_like_temp = int(weather_info['main']['feels_like'] - kelvin) # Convert from kelvin to Celsius
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

            weather = f"\n  {search_option}" \
                      f"\n  Temperature: {self.C_to_F(temp)}°F" \
                      f"\n  Temperature feels like: {self.C_to_F(feels_like_temp)}°F" \
                      f"\n  Pressure: {pressure} hPa" \
                      f"\n  Humidity: {humidity}%" \
                      f"\n  Sunrise: {sunrise_time}" \
                      f"\n  Sunset at: {sunset_time}" \
                      f"\n  Cloud: {cloudy}%" \
                      f"\n  Info: {description}"
        else:
            weather = f"\n\t'{search_option}' not found. \n Check spelling and try again."

        self.weather_response.insert(tk.INSERT, weather)
        self.weather_response.config(state='disabled')

        self.ClearText()


if __name__ == '__main__':
    app = WeatherApp()
    app.mainloop()
