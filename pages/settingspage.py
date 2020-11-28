from PyQt5 import QtWidgets, uic

qtCreatorFile = "./ui/settings.ui"  # Enter file here.
Ui_Settings, QtBaseClass = uic.loadUiType(qtCreatorFile)


class SettingsWidget(QtWidgets.QMainWindow, Ui_Settings):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Settings.__init__(self)
        self.setupUi(self)
