from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from sudoku_database_cursor import SudokuDatabaseCursor


class SelectedSudokuLeadersWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(449, 346)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
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
        Form.setWindowTitle(_translate("Form", "Лидеры по этому судоку"))


class SelectedSudokuLeadersWindow(SelectedSudokuLeadersWindowUiForm, QWidget):
    def __init__(self, parent_window):
        super(SelectedSudokuLeadersWindow, self).__init__()
        self.parent_window = parent_window
        self.setupUi(self)

        self.db_cursor = SudokuDatabaseCursor()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent_window.child_window = None
        self.close()
