DIFFICULT_LEVELS = {
    'Легко': ('EASY', (30, 35)),
    'Средне': ('STANDARD', (25, 30)),
    'Сложно': ('HARD', (20, 25))
}

SUDOKU_GENERATION_MAX_ATTEMPTS = 1000

TIMER_DELAY_FOR_PROGRESS_BAR_ANIMATION = 10

DATABASE_FOLDER = 'db'
DATABASE_FILENAME = 'sudoku_db.sqlite3'
DATABASE_INITIALIZE_SCRIPT = """CREATE TABLE matrixes (
    id             INTEGER       PRIMARY KEY AUTOINCREMENT
                                 UNIQUE
                                 NOT NULL,
    size           INTEGER       NOT NULL,
    level          INTEGER       NOT NULL,
    timestamp      INTEGER       NOT NULL,
    solved_matrix  STRING (2000) NOT NULL,
    problem_matrix STRING (2000) NOT NULL,
    status STRING (100) NOT NULL
);"""
