import requests, json
from tkinter import *
from datetime import datetime

root = Tk()
root.geometry("500x500")
root.resizable(0, 0)
root.title("JP Weather App")

textField = Text(root, width=46, height=10)
textField.delete("1.0", "end")

city_head = Label(root, text='Enter City Name', font='Arial 12 bold').pack(pady=10)
inp_city = Entry(root, textvariable=city_value, width=24, font='Arial 14 bold').pack()
Button(root,
       command=showWeather,
       text='Check Weather',
       font='Arial 10',
       bg='lightblue',
       fg='black',
       activebackground='teal',
       padx=5,
       pady=5
       ).pack(pady=20)

weather_now = Label(root, text='The Weather is:', font='Arial 12 bold').pack(pady=10)

textField.insert(INSERT, weather)
textField.pack()

root.mainloop()
