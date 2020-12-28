from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class WinWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(531, 160)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 160))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.enter_name = QtWidgets.QLineEdit(Form)
        self.enter_name.setSizeIncrement(QtCore.QSize(0, 25))
        self.enter_name.setObjectName("enter_name")
        self.verticalLayout.addWidget(self.enter_name)
        self.btn_save = QtWidgets.QPushButton(Form)
        self.btn_save.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btn_save.setObjectName("btn_save")
        self.verticalLayout.addWidget(self.btn_save)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_error = QtWidgets.QLabel(Form)
        self.label_error.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_error.setObjectName("label_error")
        self.horizontalLayout_2.addWidget(self.label_error)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_result = QtWidgets.QLabel(Form)
        self.label_result.setObjectName("label_result")
        self.horizontalLayout_2.addWidget(self.label_result)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Победа!"))
        self.label_2.setText(_translate("Form", "Введите ваше имя:"))
        self.btn_save.setText(_translate("Form", "Готово"))
        self.label_error.setText(_translate("Form", "Ошибка"))
        self.label_result.setText(_translate("Form", "Результат 231:22"))


class WinWindow(WinWindowUiForm, QWidget):
    def __init__(self):
        super(WinWindowUiForm, self).__init__()
        self.setupUi(self)
