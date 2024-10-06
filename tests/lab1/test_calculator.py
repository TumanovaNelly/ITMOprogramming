import unittest
import sys
sys.path.append('../../src')
from lab1.calculator import Calculator
from tkinter import *
from tkinter import ttk

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.output = ttk.Combobox(self.root)
        self.enter = ttk.Entry(self.root)
        self.errors = ttk.Label(self.root)
        self.buttons_frame = ttk.Frame(self.root)
        self.calculator = Calculator(self.output, self.enter, self.errors, self.buttons_frame)

    def test_add(self):
        self.enter.insert(0, "2+2")
        self.calculator.write_result()
        self.assertEqual(self.enter.get(), "4")

    def test_sub(self):
        self.enter.insert(0, "4-2")
        self.calculator.write_result()
        self.assertEqual(self.enter.get(), "2")

    def test_mul(self):
        self.enter.insert(0, "4×2")
        self.calculator.write_result()
        self.assertEqual(self.enter.get(), "8")

    def test_div(self):
        self.enter.insert(0, "4÷2")
        self.calculator.write_result()
        self.assertEqual(self.enter.get(), "2")

    def test_div_by_zero(self):
        self.enter.insert(0, "4÷0")
        self.calculator.write_result()
        self.assertEqual(self.errors["text"], "DIVISION BY ZERO")

    def test_invalid_input(self):
        self.enter.insert(0, "2+2c")
        self.calculator.write_result()
        self.assertEqual(self.errors["text"], "INCORRECT NUMBER")

    def test_memory(self):
        self.enter.insert(0, "2+2")
        self.calculator.write_result()
        self.assertEqual(self.output["values"][0], "2+2=")
        self.assertEqual(self.output.get(), "2+2=")

    def test_dlt(self):
        self.enter.insert(0, "123")
        self.calculator.dlt()
        self.assertEqual(self.enter.get(), "12")

    def test_ac(self):
        self.enter.insert(0, "123")
        self.calculator.ac()
        self.assertEqual(self.enter.get(), "")

    def test_back(self):
        self.enter.insert(0, "123")
        self.calculator.back()
        self.assertEqual(self.enter.index(INSERT), 2)

    def test_forward(self):
        self.enter.insert(0, "123")
        self.calculator.forward()
        self.assertEqual(self.enter.index(INSERT), 3)

if __name__ == "__main__":
    unittest.main()
