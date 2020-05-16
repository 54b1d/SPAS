import datetime
import sqlite3

from PyQt5 import QtWidgets, uic

from SqliteHelper import code, transactions


def add_transaction_in_ui():
    """"pops addTransaction Dialog for IN
        completes transaction and balance insertion"""
    add_trx = uic.loadUi('addTransactionDialog.ui')
    add_trx.show()
    add_trx.setWindowTitle("জমা")
    add_trx.lddate.setText(str(datetime.date.today()))

    def toggle_p_form():
        """Toggle product related form items
            based on cash RadioButton"""
        if not add_trx.rb_cash.isChecked():
            add_trx.ld_quantity.setDisabled(False)
            add_trx.ld_rate.setDisabled(False)
            add_trx.pb_calculate.setDisabled(False)
        else:
            add_trx.ld_quantity.setDisabled(True)
            add_trx.ld_rate.setDisabled(True)
            add_trx.pb_calculate.setDisabled(True)

    # trigger for toggling product fields
    add_trx.rb_cash.toggled.connect(toggle_p_form)

    # fetch names from db
    query = '''SELECT [accounts].[name], [accounts].[address], [accounts].[uid]
    FROM [accounts] ORDER BY [accounts].[name]'''
    data = code.select(query)
    for out in data:
        # out[0]=name, out[1]= address, out[2]= uid
        name, address, uid = out
        add_trx.comboBox.addItem(name + ',' + address, uid)

    def add_transaction_confirmed_in():
        uid = add_trx.comboBox.itemData(
            add_trx.comboBox.currentIndex())
        amount = add_trx.ldamount.text()
        tdate = add_trx.lddate.text()
        quantity = add_trx.ld_quantity.text()
        rate = add_trx.ld_rate.text()
        print(quantity, rate)  # debug
        desc = add_trx.tddesc.toPlainText()
        balance_receivable = 0
        balance_payable = 0
        c_in = amount
        c_out = 0
        # p_type default 0 for cash
        p_type = 0
        if add_trx.rb_rice.isChecked():
            p_type = 1
        elif add_trx.rb_oil.isChecked():
            p_type = 2
        elif add_trx.rb_oilcake.isChecked():
            p_type = 3
        elif add_trx.rb_sesame.isChecked():
            p_type = 4
        elif add_trx.rb_mustard.isChecked():
            p_type = 5

        p_quantity = 0
        if add_trx.ld_quantity.text():
            p_quantity = add_trx.ld_quantity.text()

        if uid != '' and tdate != '' and c_in != '':  # eliminates empty data
            past_balance = code.get_balance(uid)
            print('PastBalance: ' + str(past_balance))
            # Minus for cashIn to be given
            new_balance = int(past_balance) - int(c_in)
            print('New balance: ' + str(new_balance))
            if new_balance < 0:
                balance_payable = new_balance
            else:
                balance_receivable = new_balance
            print('receivable: ', abs(balance_receivable),
                  'Payable: ', abs(balance_payable))
            # update balance table
            param = (new_balance, uid)
            code.update_balance(param)

            if not p_type == 0:
                # try get previous balance
                if not code.get_inventory_balance(p_type):
                    data = (p_type, 0)
                    try:
                        code.insert_inventory(data)
                    except:
                        print("error adding inventory")
                else:
                    past_balance = code.get_inventory_balance(p_type)
                    print(past_balance)
                # try again get previous balance
                past_stock_balance = code.get_inventory_balance(p_type)
                # plus/minus to get new stock balance
                new_stock_balance = int(past_stock_balance) + int(p_quantity)
                print("New stock = " + str(new_stock_balance))
                # update with new stock balance
                param = (str(new_stock_balance), p_type)
                code.update_inventory_balance(param)

            # insert transaction
            data = (uid, tdate, desc, c_in, c_out, p_type, p_quantity, abs(
                balance_payable), abs(balance_receivable))
            if code.insert_transaction(data):
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
        else:
            add_trx.close()

    def calculate():
        """Calculate amount for quantity and rate given"""
        p_quantity = add_trx.ld_quantity.text()
        p_rate = add_trx.ld_rate.text()
        amount = int(p_quantity) * int(p_rate)
        add_trx.ldamount.setText(str(amount))

    add_trx.pb_calculate.clicked.connect(calculate)

    add_trx.accepted.connect(add_transaction_confirmed_in)


def add_transaction_out_ui():
    """"pops addTransaction Dialog for IN
        completes transaction and balance insertion"""
    add_trx = uic.loadUi('addTransactionDialog.ui')
    add_trx.setWindowTitle("খরচ")
    add_trx.lddate.setText(str(datetime.date.today()))
    add_trx.show()

    def toggle_p_form():
        """Toggle product related form items
            based on cash RadioButton"""
        if not add_trx.rb_cash.isChecked():
            add_trx.ld_quantity.setDisabled(False)
            add_trx.ld_rate.setDisabled(False)
            add_trx.pb_calculate.setDisabled(False)
        else:
            add_trx.ld_quantity.setDisabled(True)
            add_trx.ld_rate.setDisabled(True)
            add_trx.pb_calculate.setDisabled(True)

    # trigger for toggling product fields
    add_trx.rb_cash.toggled.connect(toggle_p_form)

    # fetch names from db
    query = '''SELECT [accounts].[name], [accounts].[address], [accounts].[uid]
    FROM [accounts] ORDER BY [accounts].[name]'''
    data = code.select(query)
    for out in data:
        # out[0]=name, out[1]= address, out[2]= uid
        name, address, uid = out
        add_trx.comboBox.addItem(name + ',' + address, uid)

    def add_transaction_confirmed_out():
        uid = add_trx.comboBox.itemData(
            add_trx.comboBox.currentIndex())
        amount = add_trx.ldamount.text()
        tdate = add_trx.lddate.text()
        desc = add_trx.tddesc.toPlainText()
        balance_receivable = 0
        balance_payable = 0
        c_out = amount
        c_in = 0

        # p_type default 0 for cash
        p_type = 0
        if add_trx.rb_rice.isChecked():
            p_type = 1
        elif add_trx.rb_oil.isChecked():
            p_type = 2
        elif add_trx.rb_oilcake.isChecked():
            p_type = 3
        elif add_trx.rb_sesame.isChecked():
            p_type = 4
        elif add_trx.rb_mustard.isChecked():
            p_type = 5

        p_quantity = 0
        if add_trx.ld_quantity.text():
            p_quantity = add_trx.ld_quantity.text()

        if uid != '' and tdate != '' and c_out != '':  # eliminates empty data
            past_balance = code.get_balance(uid)
            print('PastBalance: ' + str(past_balance))
            # Minus for cashIn to be given
            new_balance = int(past_balance) + int(c_out)
            print('New balance: ' + str(new_balance))
            if new_balance < 0:
                balance_payable = new_balance
            else:
                balance_receivable = new_balance
            print('receivable: ', abs(balance_receivable),
                  'Payable: ', abs(balance_payable))
            # update balance table
            param = (new_balance, uid)
            code.update_balance(param)

            if not p_type == 0:
                # try get previous balance
                if not code.get_inventory_balance(p_type):
                    data = (p_type, 0)
                    try:
                        code.insert_inventory(data)
                    except:
                        print("error adding inventory")
                else:
                    past_balance = code.get_inventory_balance(p_type)
                    print(past_balance)
                # try again get previous balance
                past_stock_balance = code.get_inventory_balance(p_type)
                # plus/minus to get new stock balance
                new_stock_balance = int(past_stock_balance) - int(p_quantity)
                print("New stock = " + str(new_stock_balance))
                # update with new stock balance
                param = (str(new_stock_balance), p_type)
                code.update_inventory_balance(param)

            # insert transaction
            data = (uid, tdate, desc, c_in, c_out, p_type, p_quantity, abs(
                balance_payable), abs(balance_receivable))
            if code.insert_transaction(data):
                msg = "সংযোজিত হয়েছে।"
                add_trx.label_msg.setText(msg)
            else:
                print("ব্যর্থ।")
        else:
            msg = "ফর্মটি যথাযথভাবে পূরণ করুন"
            add_trx.label_msg.setText(msg)
        if add_trx.rb_add_more.isChecked():
            # reset amount field
            add_trx.ldamount.setText('')
            add_trx.show()
        else:
            add_trx.close()

    def calculate():
        """Calculate amount for quantity and rate given"""
        p_quantity = add_trx.ld_quantity.text()
        p_rate = add_trx.ld_rate.text()
        amount = int(p_quantity) * int(p_rate)
        add_trx.ldamount.setText(str(amount))

    add_trx.pb_calculate.clicked.connect(calculate)
    add_trx.accepted.connect(add_transaction_confirmed_out)


def initial_adjustment():
    """Set up balance for specific account
    when running for the first time"""
    ui = uic.loadUi('init_adjustment.ui')

    # populate combobox
    query = '''SELECT [accounts].[name], [accounts].[address], [accounts].[uid]
            FROM [accounts] ORDER BY [accounts].[name]'''
    data = code.select(query)
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
            if code.update_balance(param):
                msg = str(name) + " এর হালনাগাদ সম্পন্ন। ৳" + amount
                ui.label_msg.setText(msg)
        else:
            msg = "ফর্মটি যথাযথভাবে পূরন করুন।"
            ui.label_msg.setText(msg)
        if ui.rb_add_more.isChecked():
            # reset amount field
            ui.le_amount.setText('')
            ui.show()
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


def journal():
    journalWindow = uic.loadUi('viewJournal.ui')
    """calls sqlitehelper select"""
    journalWindow.show()
    # set as requested date and day name for that
    journalWindow.label_date_day.setText(
        str(datetime.date.today()) + '- ' + str(datetime.datetime.now(
        ).strftime("%A")))
    requested_date = str(datetime.date.today)  # TODO assign date picker
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


def accounts():
    """loads accounts window"""
    # load Accountslist UI
    accountsWindow = uic.loadUi('viewAccounts.ui')
    # UI Add New Account Dialogue
    addacc = uic.loadUi('addAccountDialogue.ui')
    accountsWindow.show()

    def fetch_accounts():
        """populate accounts window table"""
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
