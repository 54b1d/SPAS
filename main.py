# Copyright SABID
# stable functions
# setup db/tables, insert account, viewAccounts,
# Trx = transaction
import datetime
import sqlite3
import sys

from functions import (accounts, add_transaction_in_ui, add_transaction_out_ui,
                       first_run, init_ledger, initial_adjustment)
from PyQt5 import QtWidgets, uic
from SqliteHelper import code

app = QtWidgets.QApplication([])
# mainWindow UI
mainUi = uic.loadUi('mainWindow.ui')

journal_window = uic.loadUi('viewJournal.ui')


# load Inventory UI
# inventoryWindow = uic.loadUi('inventory.ui')
# UI Add New Transaction


# TODO journal closing on call
def journal():
    # set as requested date and day name for that
    journal_window.label_date_day.setText(
        str(datetime.date.today()) + '- ' + str(datetime.datetime.now(
        ).strftime("%A")))
    requested_date = str(datetime.date.today)
    # TODO assign date picker to select date on fly
    requested_date = '2020-05-19'
    print("journal(): requested date predefined 19 may for debug")
    if not requested_date == '':
        query = '''SELECT
       [transactions].[trxID],
       [transactions].[uid],
       [transactions].[desc],
       [transactions].[c_in],
       [transactions].[c_out],
       [transactions].[p_type]
       FROM   [transactions]
       WHERE  [transactions].[tdate] = ?;'''
        param = (requested_date,)
        try:
            data_c = code.select(query, param)
            for x in data_c:
                trxID, uid, desc, c_in, c_out, p_type = x
                if p_type == 0:
                    if c_out:
                        print("It's c_out : ", c_out)  # debug
                        # create horizontal box with three elements
                    elif c_in:
                        print("It's c_in : ", c_in)

                else:
                    if c_out:
                        print("It's inventory out: ", c_out)

                    elif c_in:
                        print("It's inventory in: ", c_in)
        except sqlite3.Error as err:
            print(err)
    else:
        print("No date provided")
    # load Add Trx in function
    journal_window.pb_newTrx_in.clicked.connect(add_transaction_in_ui)
    # load Add Trx out function
    journal_window.pb_newTrx_out.clicked.connect(add_transaction_out_ui)
    journal_window.show()


# triggers to Create db and tables
mainUi.actionSetupdb.triggered.connect(first_run)

# trigger loads initial adjustment ui for accounts
mainUi.actionInitial_Adjustments.triggered.connect(
    initial_adjustment)

# triggers to load accounts window
mainUi.actionAccounts.triggered.connect(accounts)

# triggers to load journal window
mainUi.actionJournal.triggered.connect(journal)
# mainUi.actionInventory.triggered.connect(lambda: inventoryWindow.show())
# TODO triggers to load inventory window
# TODO add clickListener to load ledgerUi
mainUi.actionLedger.triggered.connect(init_ledger)

if __name__ == "__main__":
    mainUi.show()
    sys.exit(app.exec())
