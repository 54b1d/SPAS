from PyQt5 import QtWidgets, uic

qtCreatorFile = "./ui/reports.ui"  # Enter file here.
Ui_Reports, QtBaseClass = uic.loadUiType(qtCreatorFile)


class ReportsWidget(QtWidgets.QMainWindow, Ui_Reports):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Reports.__init__(self)
        self.setupUi(self)
