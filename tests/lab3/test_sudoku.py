import unittest

from src.lab3 import sudoku


class TestSudoku(unittest.TestCase):

    def test_group(self):
        self.assertEqual(sudoku.group([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(sudoku.group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with self.assertRaises(ValueError):
            sudoku.group([1, 2, 3, 4, 5], 3)  # Должно выбросить ошибку, так как невозможно разбить на группы по 3


    def test_read_sudoku(self):
        grid = sudoku.read_sudoku("..\..\src\lab3\puzzle1.txt")
        self.assertIsInstance(grid, list)
        self.assertEqual(len(grid), sudoku.FIELD_SIDE)
        self.assertEqual(len(grid[0]), sudoku.FIELD_SIDE)


    def test_create_grid(self):
        puzzle = "53..7....6..195...98....6.8...6...34..8.3..17...2...6.6....28...419..5....8..79.."
        grid = sudoku.create_grid(puzzle)
        self.assertEqual(len(grid), sudoku.FIELD_SIDE)
        self.assertEqual(len(grid[0]), sudoku.FIELD_SIDE)
        self.assertEqual(grid[0], ['5', '3', '.', '.', '7', '.', '.', '.', '.'])


    def test_get_row(self):
        grid = [['1', '2', '.'],
                ['4', '5', '6'],
                ['7', '8', '9']]
        self.assertEqual(sudoku.get_row(grid, (0, 0)), ['1', '2', '.'])
        self.assertEqual(sudoku.get_row(grid, (2, 0)), ['7', '8', '9'])


    def test_get_col(self):
        grid = [['1', '2', '.'],
                ['4', '5', '6'],
                ['7', '8', '9']]
        self.assertEqual(sudoku.get_col(grid, (0, 0)), ['1', '4', '7'])
        self.assertEqual(sudoku.get_col(grid, (0, 1)), ['2', '5', '8'])


    def test_get_block(self):
        grid = [['5', '3', '.', '.', '7', '.', '.', '.', '.'],
                ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
                ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
                ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
                ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
                ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
                ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
                ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
                ['.', '.', '.', '.', '8', '.', '.', '7', '9']]
        self.assertEqual(sudoku.get_block(grid, (0, 1)), ['5', '3', '.', '6', '.', '.', '.', '9', '8'])
        self.assertEqual(sudoku.get_block(grid, (4, 7)), ['.', '.', '3', '.', '.', '1', '.', '.', '6'])


    def test_find_empty_positions(self):
        grid = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        self.assertEqual(sudoku.find_empty_positions(grid), (0, 2))
        grid = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        self.assertEqual(sudoku.find_empty_positions(grid), (-1, -1))


    def test_find_possible_values(self):
        grid = sudoku.read_sudoku("..\..\src\lab3\puzzle1.txt")
        values = sudoku.find_possible_values(grid, (0, 2))
        self.assertEqual(values, {'1', '2', '4'})
        values = sudoku.find_possible_values(grid, (4, 7))
        self.assertEqual(values, {'2', '5', '9'})


    def test_solve(self):
        grid = sudoku.read_sudoku("..\..\src\lab3\puzzle1.txt")
        solution = sudoku.solve(grid)
        self.assertTrue(sudoku.check_solution(solution))


    def test_check_solution(self):
        grid = [['5', '3', '4', '6', '7', '8', '9', '1', '2'],
                ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
                ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
                ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
                ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
                ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
                ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
                ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
                ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
        self.assertTrue(sudoku.check_solution(grid))
        grid[0][0] = '4'
        self.assertFalse(sudoku.check_solution(grid))


    def test_generate_sudoku(self):
        grid = sudoku.generate_sudoku(40)
        self.assertEqual(sum(1 for row in grid for e in row if e == '.'), 41)
        self.assertTrue(sudoku.check_solution(sudoku.solve(grid)))


    # Тесты для проверки некорректных данных
    def test_invalid_type_input(self):
        with self.assertRaises(TypeError):
            sudoku.read_sudoku(123)  # Неверный тип аргумента

        with self.assertRaises(ValueError):
            sudoku.find_possible_values(["123"], (0, 0))  # Неверный тип grid


    def test_invalid_data_input(self):
        with self.assertRaises(ValueError):
            sudoku.group([1, 2, 3], 2)  # Некорректные данные, невозможно разделить список

        with self.assertRaises(IndexError):
            sudoku.get_row([['1', '2']], (1, 0))  # Неверная позиция (выход за границы)

        with self.assertRaises(ValueError):
            sudoku.solve([['1', '2'], ['3', '4']])  # Некорректный формат Судоку


if __name__ == "__main__":
    unittest.main()
