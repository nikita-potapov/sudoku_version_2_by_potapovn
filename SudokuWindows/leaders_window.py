from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from sudoku_database_cursor import SudokuDatabaseCursor


class LeadersWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(585, 626)
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
        self.setupUi(self)

        self.db_cursor = SudokuDatabaseCursor()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # TODO
        # Эту фу-ию потом надо убрать,
        # ведь нам не всегда надо будет возвращаться к начальномк окну
        self.parent_window.show()
