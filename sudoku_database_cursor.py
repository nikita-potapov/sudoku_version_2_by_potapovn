import os
import sqlite3
from settings import DATABASE_FOLDER
from settings import DATABASE_FILENAME
from settings import DATABASE_INITIALIZE_SCRIPT


class SudokuDatabaseCursor:
    def __init__(self):
        self.database_connection = None
        self.database_cursor = None

        self._is_database_exist()

    def _connect_database(self):
        """Коннектится к базе, создает курсор"""
        self.database_connection = sqlite3.connect(
            '\\'.join([DATABASE_FOLDER, DATABASE_FILENAME]))
        self.database_cursor = self.database_connection.cursor()

    def _initialize_database(self):
        """Коннектится и нициализирует базу данных"""
        self._connect_database()
        self.database_cursor.executescript(DATABASE_INITIALIZE_SCRIPT)

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
