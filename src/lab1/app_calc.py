from tkinter import ttk
from tkinter import Tk, Entry, Label, SOLID, W
from lab1.calculator import Calculator

# создание окна
window = Tk()
window.title("MegaCalculator")

# настройки окна
WINDOW_START_WIDTH = 300
WINDOW_START_HEIGHT = 400

window.minsize(width=WINDOW_START_WIDTH, height=WINDOW_START_HEIGHT)

SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()

WINDOW_START_X = (SCREEN_WIDTH // 2) - (WINDOW_START_WIDTH // 2)
WINDOW_START_Y = (SCREEN_HEIGHT // 2) - (WINDOW_START_HEIGHT // 2)

window.geometry(
    f"{WINDOW_START_WIDTH}x{WINDOW_START_HEIGHT}+{WINDOW_START_X}+{WINDOW_START_Y}"
)

# размещение полей ввода и вывода
data_frame = ttk.Frame(borderwidth=2, relief=SOLID, padding=[7, 5])
data_frame.place(relwidth=1, relheight=0.3)

input_data = Entry(master=data_frame, font=("Arial", 20, "bold"), foreground="#FF4E00")
input_data.place(rely=0.6, relwidth=1, anchor=W)

errors_label = Label(
    master=data_frame,
    font=("Arial", 10, "bold"),
    foreground="#FF4E00",
    text="enter expression",
)
errors_label.place(rely=0.9, relwidth=1, anchor=W)

memory_combobox = ttk.Combobox(
    master=data_frame, font=("Arial", 20, "bold"), state="readonly"
)
memory_combobox.place(rely=0.2, relwidth=1, anchor=W)

buttons_frame = ttk.Frame(borderwidth=2, relief=SOLID)
buttons_frame.place(rely=0.3, relwidth=1, relheight=0.7)

# магическим образом к полям прикрепляется логика калькулятора
megacalculator = Calculator(memory_combobox, input_data, errors_label, buttons_frame)

# запуск приложения
window.mainloop()
