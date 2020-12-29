# Настройки уровней сложности
# {название}: ({название в базе данных}, (минимум оставшихся ячеек, максимум оставшихся ячеек))
DIFFICULT_LEVELS = {
    'Легко': ('EASY', (30, 35)),
    'Средне': ('STANDARD', (25, 30)),
    'Сложно': ('HARD', (20, 25))
}
# Максимальное количество попыток генерации судоку при пересечении минимальной сложности
SUDOKU_GENERATION_MAX_ATTEMPTS = 1000

# Папка с базой данных
DATABASE_FOLDER = 'db'
# Название файла с базой данных
DATABASE_FILENAME = 'sudoku_db.sqlite3'
# Скрипт инициализации базы данных
DATABASE_INITIALIZE_SCRIPT = """CREATE TABLE matrixes (
    id                   INTEGER       PRIMARY KEY AUTOINCREMENT
                                       UNIQUE
                                       NOT NULL,
    difficult_level_name STRING (100)  NOT NULL,
    saved_timestamp      INTEGER       NOT NULL,
    solved_matrix        STRING (2000) NOT NULL,
    problem_matrix       STRING (2000) NOT NULL
);
CREATE TABLE records (
    id                   INTEGER      PRIMARY KEY AUTOINCREMENT
                                      UNIQUE
                                      NOT NULL,
    saved_timestamp      INTEGER      NOT NULL,
    game_time            STRING (100) NOT NULL,
    player_name          STRING (100),
    matrix_id            INTEGER      NOT NULL
                                      REFERENCES matrixes (id),
    difficult_level_name STRING (100) NOT NULL
);
CREATE TABLE saved_games (
    id                   INTEGER       PRIMARY KEY AUTOINCREMENT
                                       UNIQUE
                                       NOT NULL,
    saved_timestamp      INTEGER       NOT NULL,
    game_time            STRING (100)  NOT NULL,
    matrix_id            INTEGER       REFERENCES matrixes (id) 
                                       NOT NULL,
    difficult_level_name STRING (100)  NOT NULL,
    matrix_state         STRING (2000) NOT NULL
);

"""
# Количество миллисекунд в одной игровой секунде
GAME_TIMER_SECOND = 1000

# Настройки интерфейса
# Цвет неизменяемых ячеек судоку
COLOR_OF_SUDOKU_CONSTANT_CELLS = '#000000'
# Цвет изменяемых ячеек судоку
COLOR_OF_SUDOKU_DYNAMIC_CELLS = '#4a90e2'
# Показывать решение судоку в консоли
SHOW_SUDOKU_SOLVED_MATRIX = True
