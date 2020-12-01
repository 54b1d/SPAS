# Created watching tutorial
# Copyright SABID

import sqlite3
from setup import prerequisites


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
        # create "accounts" table which contains accounts with their
        # name, location, mobile, uid
        c.execute('''CREATE TABLE IF NOT EXISTS [accounts](
        [uid] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        [name] VARCHAR NOT NULL,
        [address] VARCHAR,
        [mobile] VARCHAR,
        [group] VARCHAR NOT NULL DEFAULT PR);''')

        c.execute('''CREATE TABLE IF NOT EXISTS "inventory" (
        "product_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "product_name"	TEXT NOT NULL,
        "p_lott"	TEXT NOT NULL UNIQUE,
        "product_quantity"	INTEGER NOT NULL DEFAULT 0,
        "cgs"	REAL NOT NULL DEFAULT 0
        );
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS "transactions" (
        "trx_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "date"	DATE NOT NULL,
        "dr_uid"	INTEGER NOT NULL,
        "cr_uid"	INTEGER NOT NULL,
        "description"	TEXT DEFAULT 'N/A',
        "amount"	REAL NOT NULL DEFAULT 0,
        "p_id"	INTEGER NOT NULL DEFAULT 0,
        "p_lott"	TEXT DEFAULT 0,
        "quantity"	NUMERIC DEFAULT 0,
        "cgs"	REAL DEFAULT 0
        );
        ''')

        c.execute('''CREATE TABLE "balance" (
        "uid"	INTEGER NOT NULL UNIQUE,
        "dr_amount"	REAL NOT NULL DEFAULT 0,
        "cr_amount"	REAL NOT NULL DEFAULT 0,
        PRIMARY KEY("uid")
        );
        ''')

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
                for result in database.select(query, param):
                    uid = result[0]
                    print(uid)
                    # create entry in balance table
                    query = '''INSERT INTO [balance]
                    VALUES (?, ?, ?)'''
                    # primary zero value for debit and credit
                    param = (uid, 0, 0)
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
        # INSERT INTO "main"."transactions"("date","dr_uid","cr_uid",
        # "description","amount","p_type", "quantity") VALUES (?,?,?,?,?,?,?);
        query = '''INSERT INTO "transactions"(
        "date","dr_uid","cr_uid","description","amount","p_id", "p_lott", "quantity", "cgs")
        VALUES (?,?,?,?,?,?,?,?,?);'''
        try:
            c.execute(query, data)
            self.conn.commit()
            print("Transaction inserted.")
            return True
        except sqlite3.Error as err:
            print(err)
            self.conn.rollback()
            return False

    def update_balance(self, param):
        # Update Balance
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
        try:
            c.execute(query, param)
        except sqlite3.Error as err:
            print(err)
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
                data = database.select(query, param)
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
                data = database.select(query, param)
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
                data = database.select(query, param)
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
            data = database.select(query, param)
            return data
        except sqlite3.Error as err:
            print(err)


dbname = str(prerequisites())
database = SqliteHelper(dbname)
