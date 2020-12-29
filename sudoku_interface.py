from itertools import product
import datetime
import random
import copy

from settings import DIFFICULT_LEVELS
from settings import SUDOKU_GENERATION_MAX_ATTEMPTS


def solve_sudoku(size, grid):
    """Интерпретация алгоритма X для решения судоку"""
    grid = copy.deepcopy(grid)
    rows_count, colums_count = size
    cells_count = rows_count * colums_count
    x_set = ([("rc", rc) for rc in product(range(cells_count), range(cells_count))] +
             [("rn", rn) for rn in product(range(cells_count), range(1, cells_count + 1))] +
             [("cn", cn) for cn in product(range(cells_count), range(1, cells_count + 1))] +
             [("bn", bn) for bn in product(range(cells_count), range(1, cells_count + 1))])
    y_set = dict()
    for r, c, n in product(range(cells_count), range(cells_count), range(1, cells_count + 1)):
        b = (r // rows_count) * rows_count + (c // colums_count)
        y_set[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]

    x_set, y_set = exact_cover(x_set, y_set)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(x_set, y_set, (i, j, n))

    count = 0
    for solution in solve(x_set, y_set, []):
        if not solution:
            return False
        for (row, col, number) in solution:
            grid[row][col] = number
        count += 1
        if count > 2:
            return False
        yield grid


def exact_cover(x_set, y_set):
    x_set = {j: set() for j in x_set}
    for i, row in y_set.items():
        for j in row:
            x_set[j].add(i)
    return x_set, y_set


def solve(x_set, y_set, solution):
    if not x_set:
        yield list(solution)
    else:
        col = min(x_set, key=lambda c: len(x_set[c]))
        for row in list(x_set[col]):
            solution.append(row)
            cols = select(x_set, y_set, row)
            count = 0
            for s in solve(x_set, y_set, solution):
                count += 1
                if count > 2:
                    yield False
                yield s
            deselect(x_set, y_set, row, cols)
            solution.pop()


def select(x_set, y_set, row):
    cols = []
    for j in y_set[row]:
        for i in x_set[j]:
            for k in y_set[i]:
                if k != j:
                    x_set[k].remove(i)
        cols.append(x_set.pop(j))
    return cols


def deselect(x_set, y_set, row, cols):
    for j in reversed(y_set[row]):
        x_set[j] = cols.pop()
        for i in x_set[j]:
            for k in y_set[i]:
                if k != j:
                    x_set[k].add(i)


class Sudoku:
    """Класс матрицы для судоку"""

    def __init__(self, size=3, level=None,
                 solved_sudoku=None, problem_sudoku=None,
                 animate_function=None, database_id=None,
                 current_sudoku_state=None, game_time=None):
        """Параметр size задает размер квадратов, на которые разбивается матрица,
        то есть конечная матрица будет иметь размер size ** 2 на size ** 2"""
        self.game_time = game_time
        self.current_sudoku_state = current_sudoku_state
        self.database_id = database_id
        self.animate_function = animate_function
        self.size = size
        self.solved_sudoku = solved_sudoku
        self.problem_sudoku = problem_sudoku
        self.difficult_level_name = level
        self.constant = True if self.solved_sudoku else False

    def initialize_matrix(self):
        self.solved_sudoku = []
        self.problem_sudoku = []

    def generate_initial_district(self, shift):
        """Генерирует и возвращает начальный район из self.size квадратных блоков со сдвигом shift"""
        initial_row = [i + 1 for i in range(self.size ** 2)]
        district = [initial_row[i * self.size + shift:] +
                    initial_row[:i * self.size + shift] for i in range(self.size)]
        return district

    def generate_initial_matrix(self):
        """Генерирует заполненную матрицу судоку"""
        self.initialize_matrix()
        for i in range(self.size):
            self.solved_sudoku += self.generate_initial_district(i)

    def transpose_matrix(self):
        """Транспонирует матрицу"""

        self.solved_sudoku = list(map(list, zip(*copy.deepcopy(self.solved_sudoku))))

    def change_rows(self):
        """Обменивает две случайные строки внутри одного района"""
        start = random.choice(range(self.size))
        variants = list(range(start * self.size, start * self.size + self.size))
        random.shuffle(variants)
        first = variants.pop()
        second = variants.pop()
        self.solved_sudoku[first], self.solved_sudoku[second] = self.solved_sudoku[second], \
                                                                self.solved_sudoku[first]

    def change_cols(self):
        """Обменивает два случайных столбца внутри одного района"""
        self.transpose_matrix()
        self.change_rows()
        self.transpose_matrix()

    def change_row_districts(self):
        """Обменивает два случайных горизонтальных района"""
        variants = list(range(self.size))
        first = random.choice(variants)
        variants.remove(first)
        second = random.choice(variants)

        for i in range(self.size):
            self.solved_sudoku[first * self.size + i], \
            self.solved_sudoku[second * self.size + i] = self.solved_sudoku[
                                                             second * self.size + i], \
                                                         self.solved_sudoku[
                                                             first * self.size + i]

    def change_col_districts(self):
        """Обменивает два случайных вертикальных района"""
        self.transpose_matrix()
        self.change_row_districts()
        self.transpose_matrix()

    def random_mix_matrix(self, k=20):
        """Совершает k случайных действий над матрицей,
         не приводящих к недопустимым позициям"""
        mix_functions = [self.transpose_matrix,
                         self.change_rows,
                         self.change_cols,
                         self.change_row_districts,
                         self.change_col_districts]

        for _ in range(k):
            mix_function = random.choice(mix_functions)
            mix_function()

    def _show_matrix_as_sudoku(self, showed_matrix):
        """Выводит матрицу в консоль в виде судоку"""
        showed_matrix = copy.deepcopy(showed_matrix)
        number_of_symbols = len(str(self.size ** 2))
        for i, row in enumerate(showed_matrix):
            for j, element in enumerate(row):
                cell_value = str(element) if element else ''
                cell_value = cell_value.rjust(number_of_symbols, ' ')
                print(' ' + cell_value + ' ', end='')
            print()
        print()

    def show_solved_matrix(self, as_matrix=False):
        """Выводит решенную матрицу в консоль"""
        if as_matrix:
            for row in self.solved_sudoku:
                print(row)
        else:
            self._show_matrix_as_sudoku(self.solved_sudoku)

    def show_problem_matrix(self, as_matrix=False):
        """Выводит нерешенную матрицу в консоль"""
        if as_matrix:
            for row in self.solved_sudoku:
                print(row)
        else:
            self._show_matrix_as_sudoku(self.problem_sudoku)

    def set_sudoku_size(self, size):
        """Устанавливает новый размер судоку матрицы,
         генерирует новую матрицу"""
        self.size = size

    def generate_sudoku(self, difficult_level_name):
        """Генерирует и возвращает судоку определенного уровня сложности difficult,
        представленным в виде кортежа наименьшего и наибольшего возможного
        количества оставшихся на поле клеток"""
        if not self.constant:
            self.difficult_level_name = difficult_level_name

            self.initialize_matrix()
            self.generate_initial_matrix()
            self.random_mix_matrix()

            problem_sudoku = self.get_solved_matrix()

            cells = self.size ** 4

            difficult_max, difficult_min = DIFFICULT_LEVELS[difficult_level_name][1]
            difficult_max = cells - difficult_max

            variants = [(row, col, problem_sudoku[row][col]) for row in range(self.size ** 2)
                        for col in range(self.size ** 2)]
            random.shuffle(variants)

            history = []

            maximum_difficult = 0
            maximum_sudoku = None

            attempts = 0
            max_attempts_count = SUDOKU_GENERATION_MAX_ATTEMPTS

            current_difficult = 0
            while current_difficult < difficult_max:
                row, col, value = variants.pop()
                problem_sudoku[row][col] = 0
                solutions = 0
                for _ in solve_sudoku((self.size, self.size), problem_sudoku):
                    solutions += 1
                if solutions == 1:
                    current_difficult += 1
                    if current_difficult > maximum_difficult:
                        maximum_difficult = current_difficult
                        maximum_sudoku = copy.deepcopy(problem_sudoku)
                    if variants:
                        history.append(((row, col, value), copy.deepcopy(problem_sudoku),
                                        copy.deepcopy(variants), current_difficult))
                else:
                    problem_sudoku[row][col] = value

                if not variants:
                    deleted, problem_sudoku, variants, current_difficult = history.pop()
                    row, col, value = deleted
                    problem_sudoku[row][col] = value

                attempts += 1
                if self.animate_function is not None:
                    self.animate_function(int((attempts * 100) / SUDOKU_GENERATION_MAX_ATTEMPTS))
                if attempts > max_attempts_count:
                    problem_sudoku = copy.deepcopy(maximum_sudoku)
                    current_difficult = maximum_difficult
                    break

            # TODO
            print('Max Target:', difficult_max, 'Max Founded:', maximum_difficult,
                  'Current:', current_difficult, 'Attempt', attempts)

            self.problem_sudoku = problem_sudoku
        else:
            problem_sudoku = copy.deepcopy(self.problem_sudoku)

        return problem_sudoku

    def get_solved_matrix(self):
        """Возвращает копию текущей заполненной матрицы"""
        return copy.deepcopy(self.solved_sudoku)

    def get_problem_matrix(self):
        """Возвращает копию текущей незаполненной матрицы"""
        return copy.deepcopy(self.problem_sudoku)

    def get_difficult_level_name(self):
        """Возвращает название уровня сложнсоти"""
        return self.difficult_level_name

    def get_size(self):
        """Возвращает размер самого маленького квадрата судоку"""
        return self.size

    def get_database_id(self):
        """Возвращает номер записи этого судоку в базе данных"""
        return self.database_id

    def get_current_sudoku_state(self):
        """Возвращает текущее состояние судоку у игрока"""
        return self.current_sudoku_state

    def set_current_state(self, matrix):
        self.current_sudoku_state = copy.deepcopy(matrix)

    def get_game_time(self):
        return self.game_time

    def set_game_time(self, game_time):
        self.game_time = game_time
