from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from settings import DIFFICULT_LEVELS
from .leaders_window import LeadersWindow
from .saved_window import SavedGamesWindow
from .game_window import GameWindow
from sudoku_interface import Sudoku
from sudoku_database_cursor import SudokuDatabaseCursor


class InitialWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(380, 540)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(122, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.label_title = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.verticalLayout.addWidget(self.label_title)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.btn_new_game = QtWidgets.QPushButton(Form)
        self.btn_new_game.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_new_game.setObjectName("btn_new_game")
        self.verticalLayout.addWidget(self.btn_new_game)

        self.new_game_difficult_levels_buttons = []
        for difficult_level_name in DIFFICULT_LEVELS:
            btn_name = f'btn_{difficult_level_name}'
            setattr(self, btn_name, QtWidgets.QPushButton(Form))
            getattr(self, btn_name).setMinimumSize(QtCore.QSize(0, 30))
            getattr(self, btn_name).setObjectName("btn_easy")
            self.verticalLayout.addWidget(getattr(self, btn_name))

            self.new_game_difficult_levels_buttons.append(getattr(self, btn_name))

        self.btn_saved_games = QtWidgets.QPushButton(Form)
        self.btn_saved_games.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_saved_games.setObjectName("btn_saved_games")
        self.verticalLayout.addWidget(self.btn_saved_games)

        self.btn_back_to_main_menu = QtWidgets.QPushButton(Form)
        self.btn_back_to_main_menu.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_back_to_main_menu.setObjectName("btn_back_to_main_menu")
        self.verticalLayout.addWidget(self.btn_back_to_main_menu)

        self.btn_leaders_table = QtWidgets.QPushButton(Form)
        self.btn_leaders_table.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_leaders_table.setObjectName("btn_records_table")
        self.verticalLayout.addWidget(self.btn_leaders_table)
        self.btn_exit = QtWidgets.QPushButton(Form)
        self.btn_exit.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_exit.setObjectName("btn_exit")
        self.verticalLayout.addWidget(self.btn_exit)

        self.progress_bar = QtWidgets.QProgressBar(Form)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout.addWidget(self.progress_bar)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(122, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Судоку"))
        self.label_title.setText(_translate("Form", "Судоку"))
        self.btn_new_game.setText(_translate("Form", "Новая игра"))

        for difficult_level_name in DIFFICULT_LEVELS:
            getattr(self, f'btn_{difficult_level_name}'). \
                setText(_translate("Form", difficult_level_name))
        self.btn_saved_games.setText(_translate("From", "Сохранения"))
        self.btn_back_to_main_menu.setText(_translate("Form", "Назад"))
        self.btn_leaders_table.setText(_translate("Form", "Рекорды"))
        self.btn_exit.setText(_translate("Form", "Выход"))


class InitialWindow(InitialWindowUiForm, QWidget):
    def __init__(self):
        super(InitialWindow, self).__init__()
        self.setupUi(self)
        self.parent_window = None
        self.child_window = None

        self.db_cursor = None

        # progress_bar по умолчанию скрыт
        self.progress_bar.hide()
        # Просто счетчик
        self.counter = 0

        # Изначально кнопки выбора сложности и нопка "Назад" скрыты
        self.hide_some_buttons()
        # Подключаем кнопки к своим функциям
        self.btn_new_game.clicked.connect(self.btn_new_game_clicked)
        self.btn_back_to_main_menu.clicked.connect(self.btn_back_to_main_menu_clicked)
        # Подключаем кнопку "Выход"
        self.btn_exit.clicked.connect(self.btn_exit_clicked)
        # Подключаем кнопку "Таблица рекордов"
        self.btn_leaders_table.clicked.connect(self.btn_leaders_table_clicked)
        # Подключаем кнопку "Сохранения"
        self.btn_saved_games.clicked.connect(self.btn_saved_games_clicked)
        # Подключаем кнопки выбора сложности
        for btn in self.new_game_difficult_levels_buttons:
            btn.clicked.connect(self.btn_new_game_difficult_level_clicked)

    def btn_new_game_clicked(self):
        self.show_some_buttons()

    def btn_new_game_difficult_level_clicked(self):
        if self.db_cursor is None:
            self.db_cursor = SudokuDatabaseCursor()

        self.show_progress_bar()
        sudoku = Sudoku(animate_function=self.progress_bar_set_value)
        sudoku.generate_sudoku(self.sender().text())

        self.db_cursor.add_sudoku_matrix(sudoku)

        self.hide_progress_bar()

        sudoku = self.db_cursor.get_last_sudoku()

        self.game_window = GameWindow(self, sudoku)
        self.game_window.show()
        self.hide()
        self.hide_some_buttons()

    def btn_back_to_main_menu_clicked(self):
        self.hide_some_buttons()

    def btn_exit_clicked(self):
        # TODO
        # Тут потом что-то будем делать перед закрытием
        self.close()

    def btn_leaders_table_clicked(self):
        self.hide()
        self.child_window = LeadersWindow(self)
        self.child_window.show()

    def btn_saved_games_clicked(self):
        self.child_window = SavedGamesWindow(self)
        self.child_window.show()
        self.hide()

    def hide_progress_bar(self):
        self.progress_bar.hide()

    def show_progress_bar(self):
        self.progress_bar.show()

    def progress_bar_set_value(self, value: int):
        self.progress_bar.setValue(value)

    def hide_some_buttons(self):
        """Скрывает кнопки выбора сложности для новой игры и кнопку 'Назад',
        и показывает обратно кнопки 'Выход' и 'Таблица рекордов'"""
        for btn in self.new_game_difficult_levels_buttons:
            btn.hide()
        self.btn_back_to_main_menu.hide()

        self.btn_exit.show()
        self.btn_leaders_table.show()
        self.btn_new_game.show()
        self.btn_saved_games.show()

    def show_some_buttons(self):
        """Показывает кнопки выбора сложности для новой игры и кнопку 'Назад',
        и скрывает кнопки 'Выход' и 'Таблица рекордов'"""
        for btn in self.new_game_difficult_levels_buttons:
            btn.show()
        self.btn_back_to_main_menu.show()

        self.btn_exit.hide()
        self.btn_leaders_table.hide()
        self.btn_new_game.hide()
        self.btn_saved_games.hide()
