import sys

from PyQt6.QtWidgets import QApplication

from src.gui.MainWindow import MainWindow

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()
    except BaseException as e:
        print(e)
