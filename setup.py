import configparser
from PyQt5 import uic
from configparser import ConfigParser
import glob


def list_databases():
    # list databases in directory
    db_list = []
    for db in glob.glob("*.db"):
        db_list.append(db)
    return db_list


def prerequisites():
    # look for config file
    config_file = 'Settings.ini'
    config_obj = ConfigParser()
    config_obj.read(config_file)
    try:
        app_settings = config_obj["APPSETTINGS"]
        dbname = app_settings["dbname"]
        if not dbname:
            init_setup_ui(config_file, config_obj)
            print("No DBNAME found")
        else:
            print("Software has a configuration file.\nContinuing...")
            return dbname
    except:
        msg = "Application is not configured"
        print(msg)
        init_setup_ui(config_file, config_obj)


def init_setup_ui(config_file, config_obj):
    setup_ui = uic.loadUi('ui/setup.ui')
    setup_ui.show()
    setup_ui.rb_use_existing_database.clicked.connect(lambda: use_existing())

    def use_existing():
        if setup_ui.rb_use_existing_database.isChecked():
            print("Checked")
            setup_ui.ld_dbname.setEnabled(False)
        else:
            print("Not checked")
            setup_ui.ld_dbname.setEnabled(True)

    databases = list_databases()
    for out in databases:
        setup_ui.combo_databases.addItem(out)

    print("Setting up application")

    setup_ui.accepted.connect(lambda: store_settings_confirmed(config_file))

    def store_settings_confirmed(config_file):
        business_name = str(setup_ui.ld_business_name.text())
        business_address = str(setup_ui.ld_business_address.text())
        if setup_ui.rb_use_existing_database.isChecked():
            dbname = str(setup_ui.combo_databases.currentText())
            print('existing', dbname)
        else:
            dbname = str(setup_ui.ld_dbname.text()) + '.db'

        # todo check if empty

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
