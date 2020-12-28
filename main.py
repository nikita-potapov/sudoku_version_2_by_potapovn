from PyQt5.QtWidgets import QApplication
import SudokuWindows
import sys

if __name__ == '__main__':
    application = QApplication(sys.argv)
    program = SudokuWindows.InitialWindow()
    program.show()
    sys.exit(application.exec())
