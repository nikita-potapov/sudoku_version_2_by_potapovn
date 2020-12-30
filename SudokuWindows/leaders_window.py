from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from sudoku_database_cursor import SudokuDatabaseCursor
from .selected_sudoku_leaders_window import SelectedSudokuLeadersWindow
from .game_window import GameWindow
from settings import DIFFICULT_LEVELS
import datetime

from settings import ICON_PATH

NORMAL = 0
EXIT = 1


class LeadersWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(380, 540)

        Form.setWindowIcon(QtGui.QIcon(ICON_PATH))

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_back = QtWidgets.QPushButton(Form)
        self.btn_back.setObjectName("btn_back")
        self.horizontalLayout.addWidget(self.btn_back)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.btn_show_rang = QtWidgets.QPushButton(Form)
        self.btn_show_rang.setObjectName("btn_show_rang")
        self.horizontalLayout.addWidget(self.btn_show_rang)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.btn_play_again = QtWidgets.QPushButton(Form)
        self.btn_play_again.setObjectName("btn_play_again")
        self.horizontalLayout.addWidget(self.btn_play_again)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.selector_difficult = QtWidgets.QComboBox(Form)
        self.selector_difficult.setObjectName("selector_difficult")
        self.horizontalLayout.addWidget(self.selector_difficult)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(Form)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Таблица рекордов"))
        self.btn_back.setText(_translate("Form", "В главное меню"))
        self.btn_show_rang.setText(_translate("Form", "Смотреть ранг"))
        self.btn_play_again.setText(_translate("Form", "Играть снова"))


class LeadersWindow(LeadersWindowUiForm, QWidget):
    def __init__(self, parent_window):
        super(LeadersWindowUiForm, self).__init__()
        self.parent_window = parent_window
        self.child_window = None
        self.game_window = None
        self.setupUi(self)

        self.status = NORMAL

        self.db_cursor = SudokuDatabaseCursor()

        # Подключаем кнопку "В главное меню"
        self.btn_back.clicked.connect(self.btn_back_clicked)

        # Подключаем кнопку "Посмотреть ранг"
        self.btn_show_rang.clicked.connect(self.btn_show_rang_clicked)

        # Подключаем кнопку "играть снова"
        self.btn_play_again.clicked.connect(self.btn_play_again_clicked)

        # Смена сложности
        self.selector_difficult.currentIndexChanged.connect(self.update_records_table)

        self.selector_difficult.addItems(['Сложность'] + list(DIFFICULT_LEVELS.keys()))

        self.update_records_table()

    def update_records_table(self):
        difficult_level_name = self.selector_difficult.currentText()
        if difficult_level_name == 'Сложность':
            difficult_level_name = ''

        records = self.db_cursor.get_all_records_games(difficult_level_name)

        records_by_sudoku = {}

        for record in records:
            sudoku_database_id = record[4]
            records_by_sudoku[sudoku_database_id] = \
                records_by_sudoku.get(sudoku_database_id, []) + [record]

        self.best_of_records = [min(values,
                                    key=lambda x: (x[1], x[2])) for values in
                                records_by_sudoku.values()]
        table = self.table

        table.setRowCount(0)
        if self.best_of_records:
            table.setColumnCount(len(self.best_of_records[0]))
            table.setHorizontalHeaderLabels(['ID',
                                             'Дата сохранения',
                                             'Время игры',
                                             'Имя игрока',
                                             'ID судоку',
                                             'Сложность'])
            for i, row in enumerate(self.best_of_records):
                table.setRowCount(table.rowCount() + 1)
                for j, value in enumerate(row):
                    if j == 1:
                        time = datetime.datetime.fromtimestamp(float(value))
                        value = time.strftime('%d-%m-%Y %H:%M:%S')
                    if j == 2:
                        seconds = int(value)
                        minutes = seconds // 60
                        hours = minutes // 60
                        seconds = seconds % 60
                        minutes = minutes % 60

                        w = [hours, minutes, seconds]
                        value = ':'.join([str(x).rjust(2, '0') for x in w])

                    item = QTableWidgetItem(str(value))
                    table.setItem(i, j, item)

            hidden_columns = [0, 4, 5]
            if not difficult_level_name:
                hidden_columns.pop()

            for col in range(len(self.best_of_records[0])):
                if col in hidden_columns:
                    table.hideColumn(col)
                else:
                    table.showColumn(col)

    def btn_back_clicked(self):
        self.return_to_parent_window()

    def return_to_parent_window(self):
        self.parent_window.show()
        self.close()

    def btn_show_rang_clicked(self):
        current = list(self.table.selectedItems())
        if current:
            row = current[0].row()
            database_sudoku_id = int(self.best_of_records[row][4])
            records = self.db_cursor.get_records_games_by_sudoku_id(database_sudoku_id)

            records.sort(key=lambda x: (-x[2], -x[1]))

            self.child_window = SelectedSudokuLeadersWindow(self, records)
            self.child_window.show()

    def btn_play_again_clicked(self):
        current = list(self.table.selectedItems())
        if current:
            row = current[0].row()
            database_sudoku_id = int(self.best_of_records[row][4])
            sudoku = self.db_cursor.get_sudoku(database_sudoku_id)
            self.status = EXIT

            self.game_window = GameWindow(self.parent_window, sudoku)
            self.close()
            self.game_window.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.status == NORMAL:
            self.parent_window.show()
        if self.child_window is not None:
            self.child_window.close()
