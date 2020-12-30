import os
import sqlite3
import datetime
from settings import DATABASE_FOLDER
from settings import DATABASE_FILENAME
from settings import DATABASE_INITIALIZE_SCRIPT
from sudoku_interface import Sudoku


class SudokuDatabaseCursor:
    def __init__(self):
        self.database_connection = None

        self._is_database_exist()

    def add_sudoku_matrix(self, sudoku):
        database_cursor = self.database_connection.cursor()

        saved_timestamp = datetime.datetime.timestamp(datetime.datetime.now())
        difficult_level_name = sudoku.get_difficult_level_name()
        solved_matrix = sudoku.get_solved_matrix()
        problem_matrix = sudoku.get_problem_matrix()

        data = {
            'saved_timestamp': saved_timestamp,
            'difficult_level_name': difficult_level_name,
            'solved_matrix': solved_matrix,
            'problem_matrix': problem_matrix
        }

        for key, value in data.items():
            if type(value) == list:
                data[key] = "'" + self._convert_matrix_to_string(value) + "'"
            else:
                data[key] = "'" + str(value) + "'"

        query = f"""INSERT INTO matrixes({', '.join(list(data.keys()))})
         VALUES ({', '.join(list(data.values()))})"""

        database_cursor.execute(query)
        self.database_connection.commit()

    def get_saved_games(self):
        database_cursor = self.database_connection.cursor()

        query = """SELECT saved_timestamp, game_time, difficult_level_name,
                        id, matrix_id, matrix_state FROM saved_games ORDER BY saved_timestamp DESC"""
        result = list(database_cursor.execute(query).fetchall())

        return result

    def add_game_record(self, sudoku, player_name):
        database_cursor = self.database_connection.cursor()
        game_time = sudoku.get_game_time()
        saved_timestamp = datetime.datetime.timestamp(datetime.datetime.now())
        matrix_id = sudoku.get_database_id()
        difficult_level_name = sudoku.get_difficult_level_name()

        data = {
            'saved_timestamp': saved_timestamp,
            'game_time': str(game_time),
            'matrix_id': matrix_id,
            'player_name': player_name,
            'difficult_level_name': difficult_level_name
        }

        for key, value in data.items():
            if type(value) == list:
                data[key] = "'" + self._convert_matrix_to_string(value) + "'"
            else:
                data[key] = "'" + str(value) + "'"

        query = f"""INSERT INTO records({', '.join(list(data.keys()))})
                 VALUES({', '.join(list(data.values()))})"""

        database_cursor.execute(query)
        self.database_connection.commit()

    def add_game_save(self, sudoku):
        database_cursor = self.database_connection.cursor()
        game_time = sudoku.get_game_time()
        saved_timestamp = datetime.datetime.timestamp(datetime.datetime.now())
        matrix_id = sudoku.get_database_id()
        current_sudoku_state = sudoku.get_current_sudoku_state()
        difficult_level_name = sudoku.get_difficult_level_name()

        data = {
            'saved_timestamp': saved_timestamp,
            'game_time': str(game_time),
            'matrix_id': matrix_id,
            'matrix_state': self._convert_matrix_to_string(current_sudoku_state),
            'difficult_level_name': difficult_level_name
        }

        for key, value in data.items():
            if type(value) == list:
                data[key] = "'" + self._convert_matrix_to_string(value) + "'"
            else:
                data[key] = "'" + str(value) + "'"

        query = f"""INSERT INTO saved_games({', '.join(list(data.keys()))})
         VALUES({', '.join(list(data.values()))})"""

        database_cursor.execute(query)
        self.database_connection.commit()

    def get_all_records_games(self, difficult_level_name):
        database_cursor = self.database_connection.cursor()

        query = f"""SELECT * FROM records WHERE difficult_level_name LIKE
         '%{difficult_level_name}%' ORDER BY saved_timestamp DESC"""
        result = list(database_cursor.execute(query).fetchall())

        return result

    def get_records_games_by_sudoku_id(self, database_sudoku_id):
        database_cursor = self.database_connection.cursor()

        query = f"""SELECT * FROM records WHERE matrix_id = {database_sudoku_id}"""
        result = list(database_cursor.execute(query).fetchall())

        return result

    def delete_saved_game(self, saved_game_id):
        database_cursor = self.database_connection.cursor()

        query = f"""DELETE FROM saved_games WHERE id == {saved_game_id}"""
        database_cursor.execute(query)

        self.database_connection.commit()

    def get_saved_game(self, saved_game_id):
        database_cursor = self.database_connection.cursor()

        query = f"""SELECT * FROM saved_games WHERE id == {saved_game_id}"""
        result = database_cursor.execute(query).fetchone()
        return result

    def get_sudoku(self, database_sudoku_id):
        database_cursor = self.database_connection.cursor()

        query = f"""SELECT * FROM matrixes WHERE id == {database_sudoku_id}"""
        result = database_cursor.execute(query).fetchone()
        sudoku = Sudoku(database_id=result[0],
                        level=result[1],
                        solved_sudoku=self._convert_string_to_matrix(result[3]),
                        problem_sudoku=self._convert_string_to_matrix(result[4]))

        return sudoku

    def get_last_sudoku(self):
        database_cursor = self.database_connection.cursor()

        query = """SELECT * FROM matrixes ORDER BY id DESC"""
        matrix = database_cursor.execute(query).fetchone()
        return Sudoku(level=matrix[1],
                      problem_sudoku=self._convert_string_to_matrix(matrix[4]),
                      solved_sudoku=self._convert_string_to_matrix(matrix[3]),
                      database_id=matrix[0])

    def convert_str_to_list(self, string):
        return self._convert_string_to_matrix(string)

    def _connect_database(self):
        """Коннектится к базе, создает курсор"""
        self.database_connection = sqlite3.connect(
            '\\'.join([DATABASE_FOLDER, DATABASE_FILENAME]))

    def _initialize_database(self):
        """Коннектится и нициализирует базу данных"""
        self._connect_database()
        database_cursor = self.database_connection.cursor()
        database_cursor.executescript(DATABASE_INITIALIZE_SCRIPT)

    def _is_database_exist(self):
        """Проверяет, существует ли база данных,
         если нет - создает новую, вызвав _initialize_database"""
        current_folder = next(os.walk(os.getcwd()))
        _, sub_folders, _ = current_folder
        if DATABASE_FOLDER in sub_folders:
            database_path = '\\'.join([os.getcwd(), DATABASE_FOLDER, DATABASE_FILENAME])
            try:
                with open(database_path):
                    pass
                self._connect_database()
            except FileNotFoundError:
                self._initialize_database()
        else:
            os.mkdir(DATABASE_FOLDER)
            self._initialize_database()

    def _convert_matrix_to_string(self, matrix):
        return '='.join(['-'.join(map(str, row)) for row in matrix])

    def _convert_string_to_matrix(self, string):
        return [[int(x) for x in row.split('-')] for row in string.split('=')]

    def __del__(self):
        self.database_connection.close()
