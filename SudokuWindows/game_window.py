from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class GameWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(498, 499)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_back = QtWidgets.QPushButton(Form)
        self.btn_back.setMinimumSize(QtCore.QSize(0, 10))
        self.btn_back.setObjectName("btn_back")
        self.horizontalLayout.addWidget(self.btn_back)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.game_time = QtWidgets.QPushButton(Form)
        self.game_time.setMinimumSize(QtCore.QSize(0, 10))
        self.game_time.setObjectName("game_time")
        self.horizontalLayout.addWidget(self.game_time)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.sudoku_layout = QtWidgets.QGridLayout()
        self.sudoku_layout.setObjectName("sudoku_layout")
        self.pushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.sudoku_layout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.sudoku_layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Судоку"))
        self.btn_back.setText(_translate("Form", "В главное меню"))
        self.game_time.setText(_translate("Form", "12:32"))
        self.pushButton.setText(_translate("Form", "PushButton"))


class GameWindow(GameWindowUiForm, QWidget):
    def __init__(self, parent_window, sudoku):
        super(GameWindowUiForm, self).__init__()
        self.sudoku = sudoku
        self.parent_window = parent_window
        self.setupUi(self)
