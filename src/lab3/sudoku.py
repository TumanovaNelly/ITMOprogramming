from random import shuffle
import pathlib
import typing as tp

T = tp.TypeVar("T")

# Константы
BLOCK_SIDE = 3
FIELD_SIDE = BLOCK_SIDE ** 2


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """
    Читает "Судоку" из указанного файла
    """
    path = pathlib.Path(path)
    with path.open() as file:
        puzzle = file.read()
    return create_grid(puzzle)


#################### только для FIELD_SIDE == 3 ####################
def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, FIELD_SIDE)
    return grid


def check_grid(grid: tp.List[tp.List[str]]) -> None:
    """
    Кидает исключения, если grid не верный
    """
    if len(grid) != FIELD_SIDE:
        raise ValueError(f"У игрового поля должно быть {FIELD_SIDE} строк")
    for line in grid:
        if len(line) != FIELD_SIDE:
            raise ValueError(f"У игрового поля должно быть {FIELD_SIDE} столбцов в каждой строке")


def display(grid: tp.List[tp.List[str]]) -> None:
    """
    Вывод "Судоку"
    """
    check_grid(grid)  # если grid не верный, тут программа кинет исключение

    width = 2
    line = "+".join(["-" * (width * BLOCK_SIDE)] * BLOCK_SIDE)
    for row in range(FIELD_SIDE):

        print(
            "".join(
                grid[row][col].center(width) + ("|" if col + 1 < FIELD_SIDE and
                                                      (col + 1) % BLOCK_SIDE == 0
                                                    else "")
                for col in range(FIELD_SIDE)
            )
        )
        if row + 1 < FIELD_SIDE and (row + 1) % BLOCK_SIDE == 0:
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """

    if len(values) % n != 0:
        raise ValueError("Невозможно разделить список на равные группы длиной n")

    return [values[start: start + n] for start in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """
    Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """

    return grid[pos[0]][:]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """
    Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """

    return [row[pos[1]] for row in grid]


def get_block(grid: tp.List[tp.List[str]], position: tp.Tuple[int, int]) -> tp.List[str]:
    """
    Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    check_grid(grid) # если grid не верный, тут программа кинет исключение

    start_row = (position[0] // BLOCK_SIDE) * BLOCK_SIDE
    start_col = (position[1] // BLOCK_SIDE) * BLOCK_SIDE
    return ([grid[row][col] for row in range(start_row, start_row + BLOCK_SIDE)
             for col in range(start_col, start_col + BLOCK_SIDE)])


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """
    Находит первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '.':
                return row, col

    return -1, -1


def find_possible_values(grid: tp.List[tp.List[str]], position: tp.Tuple[int, int]) -> tp.Set[str]:
    """
    Возвращает множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """

    return ({str(num) for num in range(1, FIELD_SIDE + 1)}
            .difference(get_block(grid, position)) # если grid не верный, тут программа кинет исключение
            .difference(get_row(grid, position))
            .difference(get_col(grid, position)))


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """
    Решение пазла, заданного в grid
    Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    empty_pos = find_empty_positions(grid)
    if empty_pos == (-1, -1):
        check_grid(grid)
        return grid

    for value in find_possible_values(grid, empty_pos):
        grid[empty_pos[0]][empty_pos[1]] = value
        solution = solve(grid)
        if solution:
            return solution
    grid[empty_pos[0]][empty_pos[1]] = '.'

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """
    Если решение solution верно, то вернуть True, в противном случае False
    """
    set_num = {str(num) for num in range(1, FIELD_SIDE + 1)}
    for row in range(0, FIELD_SIDE, 3):
        for col in range(0, FIELD_SIDE, 3):
            if not (set_num == set(get_block(solution, (row, col)))): # если solution не FIELD_SIDE на FIELD_SIDE, тут программа кинет исключение
                return False

    for i in range(FIELD_SIDE):
        if not (set_num == set(get_col(solution, (i, i)))
                == set(get_row(solution, (i, i)))):
            return False

    return True


def generate_sudoku(n: int) -> tp.List[tp.List[str]]:
    """
    Генерация "Судоку" заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    grid = solve([['.' for _ in range(FIELD_SIDE)] for _ in range(FIELD_SIDE)])

    positions = [(row, col) for row in range(FIELD_SIDE) for col in range(FIELD_SIDE)]
    shuffle(positions)

    for i in range(FIELD_SIDE ** 2 - n):
        grid[positions[i][0]][positions[i][1]] = '.'

    return grid


if __name__ == "__main__":
    for filename in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(filename)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {filename} can't be solved")
        else:
            display(solution)