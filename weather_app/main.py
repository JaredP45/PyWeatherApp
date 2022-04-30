import os
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk

import requests
from dotenv import load_dotenv


class ConvertTemp:
    def __init__(self, temp):
        self.temp = temp

    def C_to_F(self):
        return (self.temp * 1.80) + 32.00

    def F_to_C(self):
        return (self.temp - 32) / 1.80


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # App Window
        self.iconbitmap("jpaubel.ico")
        self.title("JPaubel Weather App")
        self.geometry("550x300")
        self.resizable(False, False)

        self.logo = PhotoImage(file='jpaubel.png')
        self.isClicked = False
        self.tempLabel = 'Celsius'

        # Entry
        self.city_name = tk.StringVar()

        self.app_image = tk.Label(self, image=self.logo)
        self.app_image.grid(column=0, row=0, sticky=NE)

        self.city_head = tk.Label(self, text='Weather Wizard', font='Arial 18 bold')
        self.city_head.grid(column=1, row=0, sticky=tk.NW, pady=5)

        self.city_head = tk.Label(self, text='Enter City Name', font='Arial 12')
        self.city_head.grid(column=0, row=1, padx=25, pady=5)

        self.inp_city = tk.Entry(self, textvariable=self.city_name, width=16, font='Arial 12')
        self.inp_city.grid(column=0, row=2, sticky=tk.N, padx=5)

        # Process input, call API, and display information
        tk.Button(self, command=self.retrieve_weather, text="Check Weather",
                  font="Arial 10", bg='lightblue', fg='black',
                  activebackground="teal", padx=25, pady=5).grid(column=0, row=2, sticky=tk.S)

        self.weather_now = tk.Label(self, text="The Weather is: ", font='arial 12')
        self.weather_now.grid(column=1, row=1, padx=25, pady=5)

        self.tfield = tk.Text(self, width=40, height=12)
        self.tfield.grid(column=1, row=2, padx=25, pady=5)
        self.tfield.config(state='disabled')

    @staticmethod
    def time_format_for_location(utc_with_tz):
        local_time = datetime.utcfromtimestamp(utc_with_tz)
        return local_time.time()

    def C_to_F(self, cel):
        if self.isClicked:
            self.tempLabel = "Fahrenheit"
            return (cel * 1.80) + 32.0


    def retrieve_weather(self):
        load_dotenv()
        api_key = os.environ['API_KEY']

        weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + self.city_name.get() + '&appid=' + api_key
        weather_info = requests.get(weather_url).json()

        self.tfield.config(state='normal')
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

            weather = f"\n{self.city_name.get().capitalize()}" \
                      f"\nTemperature (Celsius): {temp}°"\
                      f"\nFeels like in (Celsius): {feels_like_temp}°" \
                      f"\nPressure: {pressure} hPa" \
                      f"\nHumidity: {humidity}%" \
                      f"\nSunrise: {sunrise_time}" \
                      f"\nSunset at: {sunset_time}" \
                      f"\nCloud: {cloudy}%" \
                      f"\nInfo: {description}"
        else:
            weather = f"\n\t'{self.city_name.get()}' not found. \n Check spelling and try again."

        self.tfield.insert(tk.INSERT, weather)
        self.tfield.config(state='disabled')


if __name__ == '__main__':
    app = WeatherApp()
    app.mainloop()
