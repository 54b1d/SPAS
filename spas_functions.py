import datetime
import sqlite3

from PyQt5 import QtWidgets, uic

from SqliteHelper import database, transactions


def first_run():
    try:
        database.create_table()
    except sqlite3.Error as err:
        print(err)


def initial_adjustment():
    """Set up balance for specific account
    when running for the first time"""
    ui = uic.loadUi('init_adjustment.ui')

    # populate combobox
    query = '''SELECT [accounts].[name], [accounts].[address], [accounts].[uid]
            FROM [accounts] ORDER BY [accounts].[name]'''
    data = database.select(query)
    for out in data:
        # out[0]=name, out[1]= address, out[2]= uid
        name, address, uid = out
        ui.comboBox.addItem(name + ',' + address, uid)

    def confirmed():
        amount = ui.le_amount.text()
        name = ui.comboBox.currentText()
        uid = ui.comboBox.itemData(ui.comboBox.currentIndex())
        param = (amount, uid)
        if not amount == '':
            if database.update_balance(param):
                msg = str(name) + " এর হালনাগাদ সম্পন্ন। ৳" + amount
                ui.label_msg.setText(msg)
        else:
            msg = "ফর্মটি যথাযথভাবে পূরন করুন।"
            ui.label_msg.setText(msg)
        if ui.rb_add_more.isChecked():
            # reset amount field
            ui.le_amount.setText('')
            ui.show()
            ui.comboBox.setFocus()
        else:
            ui.close()

    ui.show()
    ui.accepted.connect(confirmed)


def ledger_transactions(uid=''):
    ledger = uic.loadUi('ledger.ui')
    # load Journal UI
    """Ledger Widget table contents"""
    data = transactions(uid)
    for row_number, row_data in enumerate(data):
        ledger.tableWidget.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            cell = QtWidgets.QTableWidgetItem(str(column_data))
            ledger.tableWidget.setItem(row_number, column_number, cell)


def accounts():
    """loads accounts window"""
    accounts_window = uic.loadUi('viewAccounts.ui')

    # UI Add New Account Dialogue
    add_acc_ui = uic.loadUi('addAccountDialogue.ui')

    def fetch_accounts():
        """populate accounts window table"""
        accounts_window.tableWidget.setRowCount(0)
        query = '''SELECT
       [accounts].[name],
       [accounts].[address],
       [accounts].[mobile],
       [balance].[dr_amount],
       [balance].[cr_amount] FROM
       [accounts]
       INNER JOIN [balance] ON [accounts].[uid] = [balance].[uid]
       ORDER BY [accounts].[name];'''

        try:
            data = database.select(query)
            # accounts_window.tableWidget.setColumnCount(2)
            for row_number, row_data in enumerate(data):
                accounts_window.tableWidget.insertRow(row_number)
                for column_number, info in enumerate(row_data):
                    celldata = QtWidgets.QTableWidgetItem(str(info))
                    accounts_window.tableWidget.setItem(
                        row_number, column_number, celldata)
        except sqlite3.Error as err:
            print('Error', err)
        accounts_window.tableWidget.setEditTriggers(
            QtWidgets.QTreeView.NoEditTriggers)

    fetch_accounts()
    accounts_window.pbViewAccountsRefresh.clicked.connect(fetch_accounts)

    def pb_add_account_clicked():
        """check/grab data and passes to sqliteHelper.insert_acc"""
        name = str(add_acc_ui.ldname.text())
        address = str(add_acc_ui.ldaddress.text())
        mobile = str(add_acc_ui.ldmobile.text())
        if name != '' and address != '':  # eliminates empty data
            data = (name, address, mobile)
            database.insert_account(data)
        else:
            print('Required fields are empty.')
            add_acc_ui.show()
        # after insert reset fields
        add_acc_ui.ldname.setText('')
        add_acc_ui.ldaddress.setText('')
        add_acc_ui.ldmobile.setText('')
        add_acc_ui.show()
        add_acc_ui.ldname.setFocus()

    # accounts_window.pbViewAccountsRefresh.clicked.connect()
    # calls function to refresh account list
    accounts_window.pbAddAccount.clicked.connect(
        add_acc_ui.show)  # opens addAcc ui
    add_acc_ui.buttonBox.accepted.connect(pb_add_account_clicked)
    accounts_window.show()


def init_ledger(uid=None):
    global ledgerUi
    ledgerUi = uic.loadUi("ledger.ui")
    query = '''SELECT
       [transactions].[tdate],
       [transactions].[c_in],
       [transactions].[c_out],
       [transactions].[balance_payable],
       [transactions].[balance_receivable]
        FROM   [transactions] WHERE [transactions].[uid] = ?
        ORDER BY [transactions].[tdate];'''
    param = (uid,)
    """data = transactions(uid)
    for row_number, row_data in enumerate(data):
        ledger.tableWidget.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            cell = QtWidgets.QTableWidgetItem(str(column_data))
            ledger.tableWidget.setItem(row_number, column_number, cell)"""
    data = database.select(query, param)
    for row_number, row_data in enumerate(data):
        t_date, c_in, c_out, balance_payable, balance_receivable = row_data
        ledgerUi.tableWidget.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            cell = QtWidgets.QTableWidgetItem(str(column_data))
            ledgerUi.tableWidget.setItem(row_number, column_number, cell)
        print(str(row_data))
    ledgerUi.show()


# get uid for specific Name supplied
def get_uid_for(name=None):
    query = '''SELECT [accounts].[uid] FROM [accounts] WHERE [name] = ?'''
    data = database.select(query, name)
    #  select uid only as int
    for x in data:
        for y in x:
            uid = y
    return uid


# trx_type == "IN" --> Cash In Flow
# else Cash Out Flow

def init_cash_transaction(trx_type=None):
    """"pops addTransaction Dialog for trx_type = IN/OUT
        based on trx_type argument provided
        completes transaction and balance insertion"""
    add_trx = uic.loadUi('ui/diagNewCashTrx.ui')
    add_trx.show()
    if trx_type == "IN":
        add_trx.setWindowTitle("নগদ জমা")
    else:
        add_trx.setWindowTitle("নগদ পরিশোধ")
    add_trx.lddate.setText(str(datetime.date.today()))

    # fetch names from db to populate dropdown list
    query = '''SELECT [accounts].[name], [accounts].[address], [accounts].[uid]
    FROM [accounts] WHERE [accounts].[group] = "PR" ORDER BY [accounts].[name];'''
    data = database.select(query)
    for out in data:
        name, address, uid = out
        add_trx.comboBox.addItem(name + ',' + address, uid)

    # declaring zero values before processing
    # todo check if cash_uid not found
    cash_uid = get_uid_for(["Cash"])

    p_id = 0  # not for cash trx
    p_lott = 0  # not for cash trx
    quantity = 0  # not for cash trx
    cgs = 0  # not for cash trx

    def cash_transaction_confirmed():
        if trx_type == "IN":
            add_trx.setWindowTitle("নগদ জমা")
            dr_uid = cash_uid
            cr_uid = add_trx.comboBox.itemData(
                add_trx.comboBox.currentIndex())
        else:
            add_trx.setWindowTitle("নগদ পরিশোধ")
            cr_uid = cash_uid
            dr_uid = add_trx.comboBox.itemData(add_trx.comboBox.currentIndex())

        amount = add_trx.ldamount.text()
        trx_date = add_trx.lddate.text()
        description = add_trx.tddesc.toPlainText()
        if description == '':
            description = "N/A"
        if dr_uid != '' and cr_uid != '' and trx_date != '' and amount != '':
            # ^^^ eliminates empty data
            # insert transaction
            values = (trx_date, dr_uid, cr_uid, description,
                      amount, p_id, p_lott, quantity, cgs)
            if database.insert_transaction(values):
                msg = "সংযোজিত হয়েছে।"
                add_trx.label_msg.setText(msg)
            else:
                print("ব্যর্থ।")
        else:
            msg = "ফর্মটি যথাযথভাবে পূরণ করুন"
            add_trx.label_msg.setText(msg)
            print('Input required Transaction in DATA')
        if add_trx.rb_add_more.isChecked():
            # reset amount field
            add_trx.ldamount.setText('')
            add_trx.show()
            add_trx.comboBox.setFocus()
        else:
            add_trx.close()

    add_trx.pb_ok.clicked.connect(cash_transaction_confirmed)
    add_trx.pb_cancel.clicked.connect(lambda: add_trx.close())


def cash_flow_in_table(self):
    # set query to select all cash in transactions with meta name
    query = '''SELECT 
       [transactions].[date], 
       [accounts].[name],
       [transactions].[amount]
FROM   [accounts]
       INNER JOIN [transactions] ON [accounts].[uid] = [transactions].[cr_uid]
        WHERE [transactions].[cr_uid] != '2' ORDER BY [transactions].[date] DESC;'''
    param = ''
    self.setRowCount(0)
    out = database.select(query, param)
    for row_number, row_data in enumerate(out):
        self.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            cell = QtWidgets.QTableWidgetItem(str(column_data))
            self.setItem(row_number, column_number, cell)


def cash_flow_out_table(self):
    # set query to select all cash out transactions with meta name
    query = '''SELECT 
       [transactions].[date], 
       [accounts].[name],
       [transactions].[amount]
FROM   [accounts]
       INNER JOIN [transactions] ON [accounts].[uid] = [transactions].[dr_uid]
        WHERE [transactions].[dr_uid] != '2' ORDER BY [transactions].[date] DESC;'''
    param = ''
    self.setRowCount(0)
    out = database.select(query, param)
    for row_number, row_data in enumerate(out):
        self.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            cell = QtWidgets.QTableWidgetItem(str(column_data))
            self.setItem(row_number, column_number, cell)
