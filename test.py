import sys

from PyQt5 import QtWidgets

from functions import initial_adjustment

app = QtWidgets.QApplication([])
initial_adjustment()
sys.exit(app.exec())
