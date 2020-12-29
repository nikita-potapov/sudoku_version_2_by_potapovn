from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from sudoku_database_cursor import SudokuDatabaseCursor
from .game_window import GameWindow
import datetime


class SavedGamesWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_back = QtWidgets.QPushButton(Form)
        self.btn_back.setObjectName("btn_back")
        self.horizontalLayout.addWidget(self.btn_back)
        self.btn_delete_saved_game = QtWidgets.QPushButton(Form)
        self.btn_delete_saved_game.setObjectName("btn_delete_saved_game")
        self.horizontalLayout.addWidget(self.btn_delete_saved_game)
        self.btn_play_saved_game = QtWidgets.QPushButton(Form)
        self.btn_play_saved_game.setObjectName("btn_play_saved_game")
        self.horizontalLayout.addWidget(self.btn_play_saved_game)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(Form)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Сохранения"))
        self.btn_back.setText(_translate("Form", "В главное меню"))
        self.btn_delete_saved_game.setText(_translate("Form", "Удалить"))
        self.btn_play_saved_game.setText(_translate("Form", "Играть"))


class SavedGamesWindow(SavedGamesWindowUiForm, QWidget):
    def __init__(self, parent_window):
        super(SavedGamesWindow, self).__init__()
        self.parent_window = parent_window
        self.setupUi(self)

        self.db_cursor = SudokuDatabaseCursor()

        self.update_saved_games_table()

        # Подключаем кнопку "В главное меню"
        self.btn_back.clicked.connect(self.btn_back_clicked)

        # Кнопка удалить
        self.btn_delete_saved_game.clicked.connect(self.btn_delete_saved_game_clicked)

        # Кнопка играть
        self.btn_play_saved_game.clicked.connect(self.btn_play_saved_game_clicked)

    def update_saved_games_table(self):
        saved_games = self.db_cursor.get_saved_games()

        table = self.table

        table.setRowCount(0)
        if saved_games:
            table.setColumnCount(len(saved_games[0]))
            table.setHorizontalHeaderLabels(['Дата сохранения',
                                             'Время игры',
                                             'Сложность',
                                             'ID',
                                             'ID судоку',
                                             'Текущее состояние'])
            for i, row in enumerate(saved_games):
                table.setRowCount(table.rowCount() + 1)
                for j, value in enumerate(row):
                    if j == 0:
                        time = datetime.datetime.fromtimestamp(float(value))
                        value = time.strftime('%d-%m-%Y %H:%M:%S')
                    if j == 1:
                        seconds = int(value)
                        minutes = seconds // 60
                        hours = minutes // 60

                        w = [hours, minutes, seconds]
                        value = ':'.join([str(x).rjust(2, '0') for x in w])

                    item = QTableWidgetItem(str(value))
                    table.setItem(i, j, item)

            for col in range(4, 6):
                table.hideColumn(col)

    def btn_back_clicked(self):
        self.close()

    def btn_delete_saved_game_clicked(self):
        current = list(self.table.selectedItems())
        if current:
            database_saved_game_id = int(current[3].text())
            self.db_cursor.delete_saved_game(database_saved_game_id)
            self.update_saved_games_table()

    def btn_play_saved_game_clicked(self):
        current = list(self.table.selectedItems())
        if current:
            database_saved_game_id = int(current[-1].text())
            saved_game = self.db_cursor.get_saved_game(database_saved_game_id)

            sudoku_database_id = int(saved_game[3])
            sudoku = self.db_cursor.get_sudoku(sudoku_database_id)
            sudoku.set_game_time(int(saved_game[2]))
            sudoku.set_current_state(self.db_cursor.convert_str_to_list(saved_game[-1]))
            self.child_window = GameWindow(self.parent_window, sudoku)
            self.hide()
            self.child_window.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent_window.show()
        self.close()
