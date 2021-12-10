import datetime
import sqlite3

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator

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


def fetch_accounts(table):
    """populate accounts window table"""
    print("Fetching accounts table items")
    table.setRowCount(0)
    query = '''SELECT 
   [accounts].[name], 
   [accounts].[address], 
   [accounts].[mobile]
    FROM   [accounts] ORDER BY [accounts].[name];'''
    try:
        data = database.select(query)
        # accounts_window.tableWidget.setColumnCount(2)
        for row_number, row_data in enumerate(data):
            table.insertRow(row_number)
            for column_number, info in enumerate(row_data):
                celldata = QtWidgets.QTableWidgetItem(str(info))
                table.setItem(
                    row_number, column_number, celldata)
    except sqlite3.Error as err:
        print('Error', err)
    table.setEditTriggers(
        QtWidgets.QTreeView.NoEditTriggers)


def fetch_inventory(table):
    """populate accounts window table"""
    print("Fetching inventory table items")
    table.setRowCount(0)
    query = '''SELECT 
   [inventory].[product_name], 
   [inventory].[product_quantity]
    FROM   [inventory] ORDER BY [inventory].[product_name];'''
    try:
        data = database.select(query)
        # accounts_window.tableWidget.setColumnCount(2)
        for row_number, row_data in enumerate(data):
            table.insertRow(row_number)
            for column_number, info in enumerate(row_data):
                celldata = QtWidgets.QTableWidgetItem(str(info))
                table.setItem(
                    row_number, column_number, celldata)
    except sqlite3.Error as err:
        print('Error', err)
    table.setEditTriggers(
        QtWidgets.QTreeView.NoEditTriggers)


def init_add_account(table):
    add_account_ui = uic.loadUi('ui/diagNewAccount.ui')
    add_account_ui.show()

    # todo get items from settings configuration
    add_account_ui.comboGroup.addItem("Payable/Receivable", "PR")

    def confirmed():
        name = add_account_ui.ld_name.text()
        address = add_account_ui.ld_address.text()
        mobile = add_account_ui.ld_mobile.text()
        group = add_account_ui.comboGroup.currentData()
        if name != '' and address != '':  # eliminates empty data
            data = (name, address, mobile, group)
            try:
                database.insert_account(data)
                msg = name + "- Added successfully."
                add_account_ui.label_msg.setText(msg)
                # after insert reset fields
                add_account_ui.ld_name.setText('')
                add_account_ui.ld_address.setText('')
                add_account_ui.ld_mobile.setText('')
                add_account_ui.ld_name.setFocus()
                fetch_accounts(table)
            except sqlite3.Error as err:
                add_account_ui.label_msg.setText(err)
        else:
            msg = 'Required fields are empty.'
            add_account_ui.show()
            add_account_ui.label_msg.setText(msg)

    add_account_ui.pb_confirm.clicked.connect(confirmed)
    add_account_ui.pb_cancel.clicked.connect(lambda: add_account_ui.close())


def init_add_product():
    add_product_ui = uic.loadUi('ui/diagNewProduct.ui')
    add_product_ui.show()
    fetch_inventory(add_product_ui.table_inventory)

    def confirmed():
        product_name = add_product_ui.ld_productName.text()
        product_lott = '0'
        if product_name != '':  # eliminates empty data
            data = (product_name, product_lott)
            try:
                database.insert_inventory(data)
                msg = product_name + " - Added successfully."
                add_product_ui.label_msg.setText(msg)
                # after insert reset fields
                add_product_ui.ld_productName.setText('')
                add_product_ui.ld_productName.setFocus()
                fetch_inventory(add_product_ui.table_inventory)
            except sqlite3.Error as err:
                add_product_ui.label_msg.setText(err)
        else:
            msg = 'Required fields are empty.'
            add_product_ui.show()
            add_product_ui.label_msg.setText(msg)

    add_product_ui.pb_confirm.clicked.connect(confirmed)
    add_product_ui.pb_cancel.clicked.connect(lambda: add_product_ui.close())


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

def init_cash_transaction(trx_tag=None):
    """"pops addTransaction Dialog for trx_type = IN/OUT
        based on trx_type argument provided
        completes transaction and balance insertion"""
    add_trx = uic.loadUi('ui/diagNewCashTrx.ui')
    add_trx.show()
    if trx_tag == "CASH_IN":
        add_trx.setWindowTitle("নগদ জমা")
    elif trx_tag == "CASH_OUT":
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
        if trx_tag == "CASH_IN":
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
            values = (trx_date, trx_tag, dr_uid, cr_uid, description,
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
        FROM   [transactions]
       INNER JOIN [accounts] ON [accounts].[uid] = [transactions].[dr_uid]
        WHERE  [transactions].[trx_tag] = 'CASH_IN' ORDER BY [transactions].[date] DESC;'''
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
        FROM   [transactions]
       INNER JOIN [accounts] ON [accounts].[uid] = [transactions].[dr_uid]
        WHERE  [transactions].[trx_tag] = 'CASH_OUT' ORDER BY [transactions].[date] DESC;'''
    param = ''
    self.setRowCount(0)
    out = database.select(query, param)
    for row_number, row_data in enumerate(out):
        self.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            cell = QtWidgets.QTableWidgetItem(str(column_data))
            self.setItem(row_number, column_number, cell)


def init_inv_transaction(trx_tag):
    def update_cgs():
        if not trx_tag == "BUY":
            product_id = ui.comboProducts.itemData(ui.comboProducts.currentIndex())
            quantity = ui.ld_quantity.text()
            cgs = get_cgs(product_id, quantity)
            ui.ld_cgs.setText(str(cgs))
        else:
            ui.ld_cgs.setText(str(0))

    def count_rate():
        # amount / quantity
        amount = ui.ld_amount.text()
        quantity = ui.ld_quantity.text()
        if amount and quantity:
            rate = float(amount) / float(quantity)
            ui.ld_rate.setText(str(rate))

    def count_amount():

        # quantity * rate = total
        # total / quantity = rate

        quantity = ui.ld_quantity.text()
        rate = ui.ld_rate.text()
        if quantity and rate:
            amount = float(quantity) * float(rate)
            ui.ld_amount.setText(str(amount))

    def count_profit():
        amount = ui.ld_amount.text()
        cgs = ui.ld_cgs.text()
        diff = float(amount) - float(cgs)
        if diff > 0:
            profit = float(diff)
            ui.ld_profit.setText(str(profit))
        elif diff < 0:
            loss = diff
            ui.ld_profit.setText(str(loss))
        else:
            balanced = diff
            ui.ld_profit.setText(str(balanced))

    def inv_trx_confirmed():
        trx_date = ui.ld_date.text()
        quantity = ui.ld_quantity.text()
        amount = ui.ld_amount.text()
        description = ui.ld_desc.text()
        p_id = ui.comboProducts.itemData(ui.comboProducts.currentIndex())
        p_lott = 'NA'
        cgs = ui.ld_cgs.text()
        if trx_tag == "BUY":
            debit_uid = ui.comboProducts.itemData(ui.comboProducts.currentIndex())
            credit_uid = ui.comboNames.itemData(ui.comboNames.currentIndex())
        else:
            debit_uid = ui.comboNames.itemData(ui.comboNames.currentIndex())
            credit_uid = ui.comboProducts.itemData(ui.comboProducts.currentIndex())
        # eliminate empty values
        if debit_uid != '' and credit_uid != '' and amount != '' and quantity != '':
            param = trx_date, trx_tag, debit_uid, credit_uid, description, amount, p_id, p_lott, quantity, cgs
            print(str(param))
            # store in database
            if database.insert_transaction(param):
                inserted = True
                msg = "Transaction added", quantity, "KG", amount, "Tk"
                ui.label_msg.setText(str(msg))
                if ui.rb_add_more.isChecked() and inserted:
                    # todo reset fields for another trx
                    ui.ld_quantity.setText('')
                    ui.ld_rate.setText('')
                    ui.ld_amount.setText('')
                    ui.ld_desc.setText('')
                    print("triggered", inserted)
            else:
                inserted = False
                msg = "Could not insert into database."
                ui.label_msg.setText(str(msg))
        else:
            msg = "Insert required values."
            ui.label_msg.setText(str(msg))

    ui = uic.loadUi('ui/diagNewInvTrx.ui')
    # set float validators
    double_validator = QDoubleValidator(0.0, 9.9, 2)
    ui.ld_quantity.setValidator(double_validator)
    ui.ld_amount.setValidator(double_validator)
    ui.ld_rate.setValidator(double_validator)
    # set window title
    if trx_tag == "BUY":
        print("Buy")
        ui.setWindowTitle("Buy Form")
    elif trx_tag == "SALE":
        print("Sale")
        ui.setWindowTitle("Sale Form")
    # set to today's date
    ui.ld_date.setText(str(datetime.date.today()))

    # fetch accounts
    query = '''SELECT [accounts].[name], [accounts].[address], [accounts].[uid]
            FROM [accounts] WHERE [accounts].[group] = "PR" ORDER BY [accounts].[name];'''
    data = database.select(query)
    # fill comboNames with accounts
    for out in data:
        name, address, uid = out
        ui.comboNames.addItem(name + ',' + address, uid)

    # fill comboProducts
    query = '''SELECT 
           [inventory].[product_id], 
           [inventory].[product_name]
            FROM   [inventory];'''
    data = database.select(query)
    for out in data:
        p_id, p_name = out
        ui.comboProducts.addItem(p_name, p_id)

    # show ui
    ui.show()

    # fill ld_cgs on comboProduct changeSignal
    ui.comboProducts.currentIndexChanged.connect(lambda: update_cgs())

    # update cgs on load
    update_cgs()

    ui.ld_quantity.textChanged.connect(update_cgs)
    ui.pb_count.clicked.connect(count_amount)
    ui.ld_amount.textChanged.connect(count_rate)
    if not trx_tag == "BUY":
        ui.ld_amount.textChanged.connect(count_profit)
    ui.pb_ok.clicked.connect(inv_trx_confirmed)
    ui.pb_cancel.clicked.connect(lambda: ui.close())


def get_cgs(p_id, quantity):
    if quantity == '':
        quantity = 0
    # get product quantity and amount
    query = '''SELECT [inventory].[product_quantity], [inventory].[cgs]
            FROM   [inventory] WHERE [inventory].[product_id] = ?;'''
    param = str(p_id)
    print("P_ID = ", p_id)
    data = database.select(query, param)
    for x, y in enumerate(data):
        gross_quantity, gross_cgs = y
    # divide them and multiply by quantity and get cgs
    cgs = float(gross_cgs) / float(gross_quantity) * float(quantity)
    print("CGS: ", cgs)
    # return cgs
    return cgs


def inventory_buy_table():
    pass


def inventory_sale_table():
    pass
