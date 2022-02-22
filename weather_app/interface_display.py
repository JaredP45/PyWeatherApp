from tkinter import *
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

import api_call as api


def weather_interface():
    root = Tk()
    root.geometry("400x400")
    root.resizable(0,0)

    root.title("JPaubel Weather App")

    city_name = StringVar()
    city_head = Label(root, text='Enter City Name', font='Arial 12 bold').pack(pady=10)
    inp_city = Entry(root, textvariable=city_name, width=24, font='Arial 14 bold').pack()

    api_call = api.WeatherAPI.weather_api_call(api.WeatherAPI(city_name.get()))
    show_weather = api.WeatherAPI.retrieve_weather(api.WeatherAPI(city_name.get()))

    Button(root, command=api_call, text="Check Weather",
           font="Arial 10", bg='lightblue', fg='black',
           activebackground="teal", padx=5, pady=5).pack(pady=20)

    weather_now = Label(root, text="The Weather is:", font='arial 12 bold')

    tfield = Text(root, width=46, height=10)

    tfield.delete("1.0", "end")

    tfield.insert(INSERT, show_weather)

    tfield.pack()

    root.mainloop()
