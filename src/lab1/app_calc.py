# -*- coding: utf-8 -*-
from tkinter import ttk
from calculator import Calculator
from tkinter import *
from tkinter import ttk

# создание окна
window = Tk()
window.title("MegaCalculator")

# настройки окна
window_start_width = 300
window_start_height = 400

window.minsize(width=window_start_width, height=window_start_height)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_start_x = (screen_width // 2) - (window_start_width // 2)
window_start_y = (screen_height // 2) - (window_start_height // 2)

window.geometry(f"{window_start_width}x{window_start_height}+{window_start_x}+{window_start_y}")

# размещение полей ввода и вывода
data_frame = ttk.Frame(borderwidth=2, relief=SOLID, padding=[7, 5])
data_frame.place(relwidth=1, relheight=0.3)

input_data = Entry(master=data_frame, font=("Arial", 20, "bold"), foreground="#FF4E00")
input_data.place(rely=0.6, relwidth=1, anchor=W)

errors_label = Label(master=data_frame, font=("Arial", 10, "bold"), foreground="#FF4E00", text="enter expression")
errors_label.place(rely=0.9, relwidth=1, anchor=W)

memory_combobox = ttk.Combobox(master=data_frame, font=("Arial", 20, "bold"), state="readonly")
memory_combobox.place(rely=0.2, relwidth=1, anchor=W)

buttons_frame = ttk.Frame(borderwidth=2, relief=SOLID)
buttons_frame.place(rely=0.3, relwidth=1, relheight=0.7)

# магическим образом к полям прикрепляется логика калькулятора
megacalculator = Calculator(memory_combobox, input_data, errors_label, buttons_frame)

# запуск приложения
window.mainloop()