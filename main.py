# Copyright SABID
# stable functions
# setup db/tables, insert account, viewaccounts,
# Trx = transaction
import sys

from PyQt5 import QtWidgets, uic

from functions import first_run, initial_adjustment, journal, accounts

app = QtWidgets.QApplication([])
# mainWindow UI
mainUi = uic.loadUi('mainWindow.ui')

# load Inventory UI
# inventoryWindow = uic.loadUi('inventory.ui')
# UI Add New Transaction
addTrx = uic.loadUi('addTransactionDialog.ui')

mainUi.actionSetupdb.triggered.connect(first_run)  # triggers to Create db and tables
mainUi.actionInitial_Adjustments.triggered.connect(
    initial_adjustment)  # trigger loads initial adjustment ui for accounts
mainUi.actionAccounts.triggered.connect(accounts)  # triggers to load accounts window
mainUi.actionJournal.triggered.connect(journal)  # triggers to load journal window

# mainUi.actionInventory.triggered.connect(lambda: inventoryWindow.show())
# TODO triggers to load inventory window
# TODO add clickListener to load ledgerUi

if __name__ == "__main__":
    mainUi.show()
    sys.exit(app.exec())
