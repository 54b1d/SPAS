from setup import prerequisites, list_databases
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
from spas_functions import first_run
from configparser import ConfigParser


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # load Main Window UI here
        uic.loadUi('ui/mainWindow.ui', self)
        self.Btn_Toggle.clicked.connect(
            lambda: UIFunctions.toggleMenu(self, 70, True))

        # list buttons available in main ui
        buttons = (self.pb_home, self.pb_cash_flow,
                   self.pb_buy_sale, self.pb_accounts,
                   self.pb_reports, self.pb_settings)

        # button actions
        for i, button in enumerate(buttons):
            button.clicked.connect(
                partial(self.stackedWidget.setCurrentIndex, i))


class SetupWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # load Main Window UI here
        uic.loadUi('ui/setup.ui', self)
        self.rb_use_existing_database.clicked.connect(lambda: use_existing())
        config_file = 'Settings.ini'
        config_obj = ConfigParser()
        config_obj.read(config_file)

        def use_existing():
            if self.rb_use_existing_database.isChecked():
                print("Checked")
                self.ld_dbname.setEnabled(False)
            else:
                print("Not checked")
                self.ld_dbname.setEnabled(True)

        databases = list_databases()
        for out in databases:
            self.combo_databases.addItem(out)

        print("Setting up application")

        self.accepted.connect(lambda: check_values(config_file))

        def check_values(config_file):
            business_name = str(self.ld_business_name.text())
            business_address = str(self.ld_business_address.text())
            if business_name != '' and business_address != '':
                store_settings_confirmed(config_file)
            else:
                msg = 'Insert required fields...'
                print(msg)
                self.label_msg.setText(msg)

        def store_settings_confirmed(config_file):
            business_name = str(self.ld_business_name.text()).replace(" ", "_")
            business_address = str(self.ld_business_address.text())
            if self.rb_use_existing_database.isChecked():
                dbname = str(self.combo_databases.currentText())
                print('existing', dbname)
            else:
                dbname = business_name + '.db'

            # store in config_file
            print(business_name, business_address, dbname)
            config_obj["USERINFO"] = {}
            user_info = config_obj["USERINFO"]
            user_info["business_name"] = business_name
            user_info["business_address"] = business_address

            config_obj["APPSETTINGS"] = {}
            app_settings = config_obj["APPSETTINGS"]
            # set as not first run
            app_settings["first_run"] = "No"
            app_settings["dbname"] = dbname
            with open(config_file, 'w') as settings:
                config_obj.write(settings)
            print("Settings Stored")


if __name__ == '__main__':
    app = QApplication([])
    # if prerequisites returns dbname then continue
    # else run setup ui
    if prerequisites():
        window = MainWindow()
        first_run()
    else:
        print("loading setup ui...")
        window = SetupWindow()
    window.show()
    app.exec_()
