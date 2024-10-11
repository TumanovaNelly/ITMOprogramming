from tkinter import Entry, Label, Button, END, INSERT
from tkinter import ttk
from decimal import Decimal
import string
import operator


class Calculator:
    def __init__(
        self,
        output_place: ttk.Combobox,
        enter_place: Entry,
        errors_place: Label,
        buttons_frame: ttk.Frame,
    ):
        self.enter = enter_place
        self.output = output_place
        self.errors = errors_place
        self.buttons_frame = buttons_frame

        # параметры кнопок
        buttons_settings = (
            (
                dict(
                    text="◀",
                    font=("Arial", 20, "bold"),
                    fg="white",
                    bg="gray",
                    command=self.back,
                ),
                dict(
                    text="▶",
                    font=("Arial", 20, "bold"),
                    fg="white",
                    bg="gray",
                    command=self.forward,
                ),
            ),
            (
                dict(
                    text="(",
                    font=("Arial", 20, "bold"),
                    fg="#FF4E00",
                    bg="white",
                    command=lambda: self.add("("),
                ),
                dict(
                    text=")",
                    font=("Arial", 20, "bold"),
                    fg="#FF4E00",
                    bg="white",
                    command=lambda: self.add(")"),
                ),
                dict(
                    text="÷",
                    font=("Arial", 26),
                    fg="#FF4E00",
                    bg="white",
                    command=lambda: self.add("÷"),
                ),
                dict(
                    text="DEL",
                    font=("Arial", 17, "bold"),
                    fg="white",
                    bg="#FF4E00",
                    command=self.dlt,
                ),
            ),
            (
                dict(
                    text="7",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("7"),
                ),
                dict(
                    text="8",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("8"),
                ),
                dict(
                    text="9",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("9"),
                ),
                dict(
                    text="×",
                    font=("Arial", 27),
                    fg="#FF4E00",
                    bg="white",
                    command=lambda: self.add("×"),
                ),
            ),
            (
                dict(
                    text="4",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("4"),
                ),
                dict(
                    text="5",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("5"),
                ),
                dict(
                    text="6",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("6"),
                ),
                dict(
                    text="+",
                    font=("Arial", 27),
                    fg="#FF4E00",
                    bg="white",
                    command=lambda: self.add("+"),
                ),
            ),
            (
                dict(
                    text="1",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("1"),
                ),
                dict(
                    text="2",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("2"),
                ),
                dict(
                    text="3",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("3"),
                ),
                dict(
                    text="-",
                    font=("Arial", 27),
                    fg="#FF4E00",
                    bg="white",
                    command=lambda: self.add("-"),
                ),
            ),
            (
                dict(
                    text="AC",
                    font=("Arial", 19, "bold"),
                    fg="white",
                    bg="#FF4E00",
                    command=self.ac,
                ),
                dict(
                    text="0",
                    font=("Arial", 20, "bold"),
                    bg="white",
                    command=lambda: self.add("0"),
                ),
                dict(
                    text=".",
                    font=("Arial", 30),
                    fg="#FF4E00",
                    bg="white",
                    command=lambda: self.add("."),
                ),
                dict(
                    text="=",
                    font=("Arial", 27, "bold"),
                    fg="white",
                    bg="#FF4E00",
                    command=self.write_result,
                ),
            ),
        )

        # размещаем кнопки
        but_lines = len(buttons_settings)
        but_height_share = 1 / (but_lines * 2 - 1)
        for row in range(but_lines):
            but_columns = len(buttons_settings[row])
            but_width_share = 1 / but_columns
            for column in range(but_columns):
                button = Button(
                    master=self.buttons_frame, **buttons_settings[row][column]
                )
                button.place(
                    relx=column * but_width_share,
                    rely=but_height_share * 2 * row
                    - (but_height_share if row > 0 else 0),
                    relwidth=but_width_share,
                    relheight=but_height_share * (2 if row > 0 else 1),
                )

        # Разрешаем ввод только определенных символов
        allowed__add_func = (
            {  # клавиши, после нажатия на которые будет вызываться функция add()
                "parenleft": "(",
                "parenright": ")",
                "plus": "+",
                "minus": "-",
                "slash": "÷",
                "asterisk": "×",
                "period": ".",
                "0": "0",
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "4",
                "5": "5",
                "6": "6",
                "7": "7",
                "8": "8",
                "9": "9",
            }
        )

        def disable_entry(event):
            if event.keysym in allowed__add_func:
                self.add(allowed__add_func[event.keysym])
            elif event.keysym == "Return" or event.keysym == "equal":
                self.write_result()
            elif event.keysym == "BackSpace":
                self.dlt()
            elif event.keysym == "Delete":
                self.ac()
            elif event.keysym == "Left":
                self.back()
            elif event.keysym == "Right":
                self.forward()

            return "break"

        self.enter.bind("<Key>", disable_entry)
        self.enter.focus()

        # При выборе ранее введенных выражений из combobox они будут вставляться в enter
        def selected(event):
            selection = self.output.get()
            self.ac()
            self.enter.insert(0, selection[:-1])

        self.output.bind("<<ComboboxSelected>>", selected)

    # ________________________________________________________________
    # функции, срабатывающие при нажатии кнопок
    def add(self, symbol):
        expression = self.enter.get()
        cursor_position = self.enter.index(INSERT)

        if symbol in string.digits:
            if (
                cursor_position < self.enter.index(END)
                and expression[cursor_position] == "("
            ):
                self.enter.insert(INSERT, "×")  # перед ( вставляется ×
                self.enter.icursor(cursor_position)
            if cursor_position > 0 and expression[cursor_position - 1] == ")":
                self.enter.insert(INSERT, "×")  # после ) вставляется ×

        if symbol == "(":
            if (
                cursor_position < self.enter.index(END)
                and expression[cursor_position] in ".×÷"
            ):  # после ( не может быть .×÷
                return
            if cursor_position > 0 and (
                expression[cursor_position - 1] in string.digits
                or expression[cursor_position - 1] in ".)"
            ):  # перед ( вставляется ×
                self.enter.insert(INSERT, "×")

        if symbol == ")":
            if (
                cursor_position > 0
                and expression[cursor_position - 1] in self.OPERATORS
            ):
                return  # нельзя поставить ) после оператора

            if cursor_position < self.enter.index(END):
                if expression[cursor_position] == ".":
                    return  # нельзя поставить ) перед точкой

                if (
                    expression[cursor_position] in string.digits
                    or expression[cursor_position] == "("
                ):
                    self.enter.insert(
                        INSERT, "×"
                    )  # если следующий символ - число, добавится ×
                    self.enter.icursor(cursor_position)

        if symbol in self.OPERATORS:
            if symbol in "×÷" and (
                cursor_position == 0 or expression[cursor_position - 1] == "("
            ):
                return  # нельзя ставить операторы ×÷ в начале или после (

            if (
                cursor_position > 0
                and expression[cursor_position - 1] in self.OPERATORS
            ):
                if (
                    cursor_position == 1 or expression[cursor_position - 2] == "("
                ) and symbol in "×÷":
                    return  # нельзя ставить ×÷ в начале и после (
                self.enter.delete(cursor_position - 1)
                self.enter.icursor(
                    cursor_position - 1
                )  # если предыдущий символ оператор и вставляется также оператор, то предыдущий заменяется на новый

            if cursor_position < self.enter.index(END):
                if (
                    expression[cursor_position] == "."
                ):  # перед точкой операторы не ставим
                    return
                if expression[cursor_position] in self.OPERATORS:
                    if (
                        cursor_position == 0 or expression[cursor_position - 1] == "("
                    ) and symbol in "×÷":
                        return
                    self.enter.delete(cursor_position)

        if symbol == ".":
            cur = cursor_position - 1
            while cur >= 0 and expression[cur] in string.digits:
                cur -= 1
            if (
                cur == cursor_position - 1 or cur >= 0 and expression[cur] == "."
            ):  # если перед точкой нет цифр или до уже ставилась точка в текущем числе
                return

            cur = cursor_position
            while cur < self.enter.index(END) and expression[cur] in string.digits:
                cur += 1
            if (
                cur < self.enter.index(END) and expression[cur] == "."
            ):  # если после уже ставилась точка в этом числе
                return

        self.enter.insert(INSERT, symbol)

    def dlt(self):
        cursor_position = self.enter.index(INSERT) - 1
        if cursor_position < 0:
            return

        expression = self.enter.get()
        symbol = expression[cursor_position]

        if (
            symbol
            in string.digits  # если удаляем цифру и перед ней больше нет цифр, а после нее стоит точка, заменяем эту цифру на ноль    ...+|1.234 -> ...+|10.234 -> ...+|0.234             "|" - позиция курсора
            and (
                cursor_position == 0
                or expression[cursor_position - 1] not in string.digits
            )
            and cursor_position < self.enter.index(END) - 1
            and expression[cursor_position + 1] == "."
        ):
            self.enter.insert(cursor_position + 1, "0")

        if (cursor_position == 0 or expression[cursor_position - 1] == "(") and (
            cursor_position < self.enter.index(END) - 1
            and expression[cursor_position + 1] in "×÷"
        ):
            self.enter.delete(
                cursor_position + 1
            )  # если до ничего нет или стоит (, а после идут оператор ×÷, этот оператор тоже удаляется

        if symbol in self.OPERATORS and 0 < cursor_position < self.enter.index(END) - 1:
            dots = False
            cur = cursor_position - 1
            while cur >= 0 and expression[cur] in string.digits:
                cur -= 1
            if cur >= 0 and expression[cur] == ".":
                dots = True

            cur = cursor_position + 1
            while cur < self.enter.index(END) and expression[cur] in string.digits:
                cur += 1
            if cur < self.enter.index(END) and expression[cur] == "." and dots:
                self.enter.delete(
                    cur
                )  # если оператор между дробными числами, они соединяются в одно дробное число, иначе оператор просто удаляется

        self.enter.delete(cursor_position)

    def ac(self):
        self.enter.delete(0, END)

    def back(self):
        cursor_position = self.enter.index(INSERT)
        if cursor_position > 0:
            self.enter.icursor(cursor_position - 1)

    def forward(self):
        cursor_position = self.enter.index(INSERT)
        if cursor_position < self.enter.index(END):
            self.enter.icursor(cursor_position + 1)

    memory = []

    def write_result(self):
        self.memory.append(self.enter.get() + "=")
        self.ac()
        self.output["values"] = self.memory
        self.output.set(self.memory[-1])

        message = str()
        try:
            self.enter.insert(0, self.get_answer(self.memory[-1][:-1]))
        except ValueError:
            message = "INCORRECT NUMBER"
        except ZeroDivisionError:
            message = "DIVISION BY ZERO"
        except:
            message = "ERROR"

        self.errors["text"] = message

    # парсер математических выражений (алгоритм сортировочной станции)
    OPERATORS = {
        "+": (1, operator.add),
        "-": (1, operator.sub),
        "×": (2, operator.mul),
        "÷": (2, operator.truediv),
    }

    # def eval():
    def get_answer(self, formula):
        def parse(formula_string):
            number = []

            for i in range(len(formula_string)):
                if formula_string[i] in string.digits or formula_string[i] == ".":
                    if i > 0 and formula_string[i - 1] == ")":
                        yield "×"

                    number.append(formula_string[i])
                elif formula_string[i] in "+-" and (
                    i == 0 or formula_string[i - 1] == "("
                ):
                    number.append(formula_string[i])
                elif formula_string[i] in self.OPERATORS or formula_string[i] in "()":
                    if number:
                        yield Decimal("".join(number))
                        number.clear()

                    if (
                        formula_string[i] == "("
                        and i > 0
                        and (
                            formula_string[i - 1] in string.digits
                            or formula_string[i - 1] in ".)"
                        )
                    ):
                        yield "×"

                    yield formula_string[i]
                else:
                    raise ValueError()
            if number:
                yield Decimal("".join(number))

        def shunting_yard(parsed_formula):
            stack = []
            for token in parsed_formula:
                if token in self.OPERATORS:
                    while (
                        stack
                        and stack[-1] != "("
                        and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]
                    ):
                        yield stack.pop()
                    stack.append(token)
                elif token == ")":
                    while stack:
                        value = stack.pop()
                        if value == "(":
                            break
                        yield value
                elif token == "(":
                    stack.append(token)
                else:
                    yield token
            while stack:
                yield stack.pop()

        def calc(polish):
            stack = []
            for token in polish:
                if token in self.OPERATORS:
                    value2, value1 = stack.pop(), stack.pop()
                    stack.append(self.OPERATORS[token][1](value1, value2))
                else:
                    stack.append(token)
            return stack[0]

        return calc(shunting_yard(parse(formula)))