import sys
from control import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    currentExitCode = MainWindow.EXIT_CODE_REBOOT
    while currentExitCode == MainWindow.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        currentExitCode = app.exec_()
        app = None

