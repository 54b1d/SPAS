from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from spas_functions import init_cash_transaction, cash_flow_in_table, cash_flow_out_table


class CashFlow(QWidget):
    # Class name is important as its imported
    # to __main__ as it is

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/cashFlow.ui', self)

        # load table data
        cash_flow_in_table(self.table_cash_flow_in)
        cash_flow_out_table(self.table_cash_flow_out)
        # button actions
        self.pb_add_trx_in.clicked.connect(lambda: init_cash_transaction("IN"))
        self.pb_add_trx_out.clicked.connect(lambda: init_cash_transaction())
        # refresh table data
        self.pb_cash_flow_refresh.clicked.connect(
            lambda: cash_flow_in_table(self.table_cash_flow_in))
        self.pb_cash_flow_refresh.clicked.connect(
            lambda: cash_flow_out_table(self.table_cash_flow_out))
