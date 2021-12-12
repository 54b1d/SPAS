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
            print("No DBNAME found")
        else:
            print("Software has a configuration file.\nContinuing...")
            return dbname
    except:
        msg = "Application is not configured"
        print(msg)
