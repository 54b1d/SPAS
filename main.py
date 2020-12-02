from setup import prerequisites
from functools import partial
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                          QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap,
                         QRadialGradient)

from ui_functions import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # load Main Window UI here
        uic.loadUi('ui/mainWindow.ui', self)
        self.Btn_Toggle.clicked.connect(
            lambda: UIFunctions.toggleMenu(self, 250, True))

        # list buttons available in main ui
        buttons = (self.pb_home, self.pb_cash_flow, self.pb_buy_sale)

        # button actions
        for i, button in enumerate(buttons):
            button.clicked.connect(
                partial(self.stackedWidget.setCurrentIndex, i))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    if prerequisites():
        window.show()
    app.exec_()
