# todo list c_in only in jounral


import sys

from functions import init_ledger
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QGroupBox
from SqliteHelper import code

app = QtWidgets.QApplication([])
ui = uic.loadUi("test.ui")
qss = "style.qss"
with open(qss, "r") as fh:
    ui.setStyleSheet(fh.read())
requested_date = '2020-05-19'
query = '''SELECT
       [transactions].[trxID],
       [accounts].[name],
       [accounts].[address],
       [transactions].[desc],
       [transactions].[c_in],
       [transactions].[c_out],
       [transactions].[p_quantity],
       [transactions].[p_type]
FROM   [transactions]
       INNER JOIN [accounts] ON [transactions].[uid] = [accounts].[uid]

WHERE  [transactions].[tdate] = ?;'''
param = (requested_date,)
data = code.select(query, param)


vbox_c_in = QVBoxLayout()
ui.groupBox_c_in.setLayout(vbox_c_in)
vbox_c_out = QVBoxLayout()
ui.groupBox_c_out.setLayout(vbox_c_out)

c_in_total = 0
c_out_total = 0
for x, row in enumerate(data):
    trxId, name, address, desc, c_in, c_out, p_quantity, p_type = row
    print(x, name, address, c_in, c_out)
    c_in_total = c_in_total + c_in
    c_out_total = c_out_total + c_out
    hbox_trx = QHBoxLayout()
    if c_in > 0:
        vbox_c_in.addLayout(hbox_trx)
    elif c_out > 0:
        vbox_c_out.addLayout(hbox_trx)
    vbox = QVBoxLayout()
    hbox_trx.addLayout(vbox)
    vbox.addWidget(QLabel(str(name)))
    vbox.addWidget(QLabel(str(address)))
    if c_in > 0:
        hbox_trx.addWidget(QLabel(str(c_in)))
    elif c_out > 0:
        hbox_trx.addWidget(QLabel(str(c_out)))

print("জমাঃ " + str(c_in_total) + "খরচঃ " + str(c_out_total))



ui.show()
sys.exit(app.exec())
