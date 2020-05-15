# Created watching tutorial
# Copyright SABID

import sqlite3


class SqliteHelper:
    def __init__(self, dbname=None):
        self.conn = None
        self.cursor = None

        if dbname:
            self.open(dbname)

    def open(self, dbname):
        try:
            self.conn = sqlite3.connect(dbname)
            self.cursor = self.conn.cursor()
            print('Sqlite version ' + sqlite3.version)
        except sqlite3.Error as err:
            print("Failed connecting to database..", err)

    def create_table(self):
        c = self.cursor
        c.execute('''CREATE TABLE [transactions](
        [trxID] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        [uid] INTEGER NOT NULL,
        [tdate] DATE NOT NULL,
        [desc] TEXT,
        [c_in] REAL NOT NULL DEFAULT 0,
        [c_out] REAL DEFAULT 0,
        [p_quantity] INT DEFAULT 0,
        [p_type] INT NOT NULL DEFAULT 0,
        [balance_payable] REAL DEFAULT 0,
        [balance_receivable] REAL DEFAULT 0);
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS [accounts](
        [uid]   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        [name]  TEXT NOT NULL,
        [address]   TEXT NOT NULL,
        [mobile]    TEXT);''')

        c.execute('''CREATE TABLE [balance](
        [uid] INT NOT NULL UNIQUE,
        [balance_amount] REAL NOT NULL DEFAULT 0);''')

        c.execute('''CREATE TABLE [inventory_balance](
        [p_type] INT NOT NULL UNIQUE,
        [p_stock] INT DEFAULT 0);''')
        print('Tables created successfully.')
        self.conn.commit()

    def insert_account(self, data):
        """Insert Account Information with balance table entry"""
        c = self.cursor
        query = '''INSERT INTO [accounts] ([name], [address], [mobile])
                VALUES (?, ? ,?)'''
        try:
            c.execute(query, data)
            try:
                query = '''SELECT [accounts].[uid]
                FROM [accounts] WHERE ROWID = ?'''
                param = (c.lastrowid,)
                for result in code.select(query, param):
                    uid = result[0]
                    print(uid)
                    # create entry in balance table
                    query = '''INSERT INTO [balance]
                    VALUES (?, ?)'''
                    param = (uid, 0)
                    try:
                        c.execute(query, param)
                        print("balance entry created with 0 balance")
                    except sqlite3.Error as err:
                        print(err)
            except sqlite3.Error as err:
                print(err)
            self.conn.commit()
            print("Account information inserted successfully.")
        except sqlite3.Error as err:
            print(err)
            self.conn.rollback()

    def insert_inventory(self, data):
        c = self.cursor
        query = '''INSERT INTO [inventory_balance] VALUES (?, ?)'''
        try:
            c.execute(query, data)
            self.conn.commit()
            print("p_type added to stock")
            return True
        except sqlite3.Error as err:
            print(err)
            self.conn.rollback()
            return False

    # todo make uid tuple
    def insert_transaction(self, data):
        """Insert transaction information"""
        c = self.cursor
        # data = ('2', '2020-04-20', '5000')
        query = '''INSERT INTO [transactions] (
            [uid], [tdate], [desc], [c_in], [c_out], [p_type], [p_quantity],
            [balance_payable], [balance_receivable])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        try:
            c.execute(query, data)
            self.conn.commit()
            print("Transaction inserted.")
            return True
        except sqlite3.Error as err:
            print(err)
            self.conn.rollback()
            return False

    def update_balance(self, param):  # Update Balance
        c = self.cursor
        query = '''UPDATE [balance] SET [balance_amount] = ? WHERE [uid] = ?'''
        try:
            c.execute(query, param)
            self.conn.commit()
            print("Balance Updated [code.update_balance]")
            return True
        except sqlite3.Error as err:
            print(err)
            self.conn.rollback()
            return False

    def update_inventory_balance(self, param):
        """update inventory stock balance"""
        c = self.cursor
        query = '''UPDATE [inventory_balance] SET [p_stock] = ? WHERE [p_type] = ?'''
        try:
            c.execute(query, param)
            self.conn.commit()
            print("Inventory Balance Updated")
        except sqlite3.Error as err:
            print(err)
            self.conn.rollback()

    def select(self, query, param=''):
        """Select"""
        c = self.cursor
        c.execute(query, param)
        return c.fetchall()

    def get_balance(self, uid=''):
        """Get balance for an uid"""
        query = '''SELECT [balance].[balance_amount] from [balance] WHERE [uid]=?'''
        param = (uid,)
        result = self.select(query, param)
        for x in result:
            balance = x[0]
            return balance

    def get_inventory_balance(self, p_type=''):
        """Get balance for an uid"""
        query = '''SELECT [inventory_balance].[p_stock] from [inventory_balance] WHERE [p_type]=?'''
        param = (p_type,)
        result = self.select(query, param)
        for x in result:
            balance = x[0]
            return balance


# call as GetMeta.name(uid)
class GetMeta():
    """get name, address, mobile"""

    def name(uid=''):
        query = '''SELECT [accounts].[name] FROM [accounts] WHERE [uid] = ?'''
        param = (str(uid))
        if uid:
            try:
                data = code.select(query, param)
                for name in data:
                    return name[0]
            except sqlite3.Error as err:
                print(err)
        else:
            print('No uid provided for GetMeta.name')

    def address(uid=''):
        query = '''SELECT [accounts].[address]
        FROM [accounts] WHERE [uid] = ?'''
        param = (str(uid))
        if uid:
            try:
                data = code.select(query, param)
                for address in data:
                    return address[0]
            except sqlite3.Error as err:
                print(err)
        else:
            print('No uid provided for GetMeta.address')

    def mobile(uid=''):
        query = '''SELECT [accounts].[mobile]
        FROM [accounts] WHERE [uid] = ?'''
        param = (str(uid))
        if uid:
            try:
                data = code.select(query, param)
                for mobile in data:
                    return mobile[0]
            except sqlite3.Error as err:
                print(err)
        else:
            print('No uid provided for GetMeta.mobile')


# transactions for specific uid, returns as list 'data'
def transactions(uid=''):
    if not uid:
        print('uid not provided for transactions')
    else:
        param = str(uid)
        query = '''SELECT
        [transactions].[tdate],
        [transactions].[c_in],
        [transactions].[c_out],
        [transactions].[balance_payable],
        [transactions].[balance_receivable]
        FROM transactions WHERE "uid" = ? ORDER BY [tdate]'''
        try:
            data = code.select(query, param)
            return data
        except sqlite3.Error as err:
            print(err)


code = SqliteHelper("MVOM.DB")
