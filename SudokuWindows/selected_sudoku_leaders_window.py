from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from settings import ICON_PATH
import datetime


class SelectedSudokuLeadersWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(380, 300)

        Form.setWindowIcon(QtGui.QIcon(ICON_PATH))

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(Form)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Лидеры по этому судоку"))


class SelectedSudokuLeadersWindow(SelectedSudokuLeadersWindowUiForm, QWidget):
    def __init__(self, parent_window, records):
        super(SelectedSudokuLeadersWindow, self).__init__()
        self.records = records
        self.parent_window = parent_window
        self.setupUi(self)

        self.update_records_table()

    def update_records_table(self):
        table = self.table
        table.setColumnCount(len(self.records[0]))
        table.setHorizontalHeaderLabels(['ID',
                                         'Дата сохранения',
                                         'Время игры',
                                         'Имя игрока',
                                         'ID судоку',
                                         'Сложность'])
        for i, row in enumerate(self.records):
            table.setRowCount(table.rowCount() + 1)
            for j, value in enumerate(row):
                if j == 1:
                    time = datetime.datetime.fromtimestamp(float(value))
                    value = time.strftime('%d-%m-%Y %H:%M:%S')
                if j == 2:
                    seconds = int(value)
                    minutes = seconds // 60
                    hours = minutes // 60
                    minutes = minutes % 60
                    seconds = seconds % 60

                    w = [hours, minutes, seconds]
                    value = ':'.join([str(x).rjust(2, '0') for x in w])

                item = QTableWidgetItem(str(value))
                table.setItem(i, j, item)

        hidden_columns = [0, 4, 5]

        for col in range(len(self.records[0])):
            if col in hidden_columns:
                table.hideColumn(col)
            else:
                table.showColumn(col)
