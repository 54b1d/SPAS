# Created watching tutorial
# Copyright SABID
# stable functions
# setup db/tables, insert account, viewaccounts,
# Trx = transaction
import datetime
import sqlite3

from PyQt5 import QtWidgets, uic

from SqliteHelper import code, transactions
from functions import add_transaction_in_ui, add_transaction_out_ui, initial_adjustment

app = QtWidgets.QApplication([])
# load mainWindow
mainUi = uic.loadUi('mainWindow.ui')
# load Accountslist UI
accountsWindow = uic.loadUi('viewAccounts.ui')
ledger = uic.loadUi('ledger.ui')
# load Journal UI
journalWindow = uic.loadUi('viewJournal.ui')
# load Inventory UI
# inventoryWindow = uic.loadUi('inventory.ui')
# UI Add New Account Dialogue
addacc = uic.loadUi('addAccountDialogue.ui')
# UI Add New Transaction
addTrx = uic.loadUi('addTransactionDialog.ui')


def journal():
    """calls sqlitehelper select"""
    journalWindow.show()
    # set current date day on top
    journalWindow.label_date_day.setText(
        str(datetime.date.today()) + '- ' + str(datetime.datetime.now(
        ).strftime("%A")))
    requested_date = str(datetime.date.today)  # todo assign date picker
    query = '''SELECT * FROM [transactions] WHERE [tdate] = ?;'''
    param = (requested_date,)
    try:
        data = code.select(query, param)
        print(data)  # debug
    except sqlite3.Error as e:
        print(e)

    # load Add Trx in function
    journalWindow.pb_newTrx_in.clicked.connect(add_transaction_in_ui)
    # load Add Trx out function
    journalWindow.pb_newTrx_out.clicked.connect(add_transaction_out_ui)


def accounts():  # loads accounts window
    accountsWindow.show()

    def fetch_accounts():
        accountsWindow.tableWidget.setRowCount(0)
        query = '''SELECT * FROM accounts'''
        try:
            data = code.select(query)
            # accountsWindow.tableWidget.setColumnCount(2)
            for row_number, row_data in enumerate(data):
                accountsWindow.tableWidget.insertRow(row_number)
                for column_number, info in enumerate(row_data):
                    celldata = QtWidgets.QTableWidgetItem(str(info))
                    accountsWindow.tableWidget.setItem(
                        row_number, column_number, celldata)
        except sqlite3.Error as e:
            print('Error', e)
        accountsWindow.tableWidget.setEditTriggers(
            QtWidgets.QTreeView.NoEditTriggers)

    fetch_accounts()
    accountsWindow.pbViewAccountsRefresh.clicked.connect(fetch_accounts)

    def pbaddaccount_clicked():
        """check/grab data and passes to sqliteHelper.insert_acc"""
        name = str(addacc.ldname.text())
        address = str(addacc.ldaddress.text())
        mobile = str(addacc.ldmobile.text())
        if name != '' and address != '':  # eliminates empty data
            data = (name, address, mobile)
            code.insert_account(data)
        else:
            print('Required fields are empty.')
            addacc.show()
        # after insert reset fields
        addacc.ldname.setText('')
        addacc.ldaddress.setText('')
        addacc.ldmobile.setText('')
        addacc.show()
        addacc.ldname.setFocus()

    # accountsWindow.pbViewAccountsRefresh.clicked.connect()
    # calls function to refresh account list
    accountsWindow.pbAddAccount.clicked.connect(addacc.show)  # opens addAcc ui
    addacc.buttonBox.accepted.connect(pbaddaccount_clicked)


def ledger_transactions(uid=''):
    """Ledger Widget table contents"""
    data = transactions(uid)
    for row_number, row_data in enumerate(data):
        ledger.tableWidget.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            cell = QtWidgets.QTableWidgetItem(str(column_data))
            ledger.tableWidget.setItem(row_number, column_number, cell)


mainUi.actionSetupdb.triggered.connect(
    code.create_table)  # triggers to Create db and tables
mainUi.actionInitial_Adjustments.triggered.connect(
    initial_adjustment)  # trigger loads initial adjustment ui for accounts
mainUi.actionAccounts.triggered.connect(
    lambda: accounts())  # triggers to load accounts window
mainUi.actionJournal.triggered.connect(
    lambda: journal())  # triggers to load journal window

# mainUi.actionInventory.triggered.connect(lambda: inventoryWindow.show())
# triggers to load inventory window
# todo add clickListener to load ledgerUi

if __name__ == "__main__":
    mainUi.show()
    app.exec()
