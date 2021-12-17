from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from spas_functions import init_inv_transaction, fetch_inventory, fetch_inventory_transactions, init_add_product


class BuySale(QWidget):
    # Class name is important as its imported
    # to __main__ as it is

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/buySale.ui', self)

        def refresh_page(self):
            fetch_inventory(self.table_inventory)
            fetch_inventory_transactions('BUY', self.table_inventory_buy)
            fetch_inventory_transactions('SALE', self.table_inventory_sale)

        refresh_page(self)
        self.pb_buy.clicked.connect(lambda: init_inv_transaction("BUY"))
        self.pb_sale.clicked.connect(lambda: init_inv_transaction("SALE"))
        self.pb_add_new_product.clicked.connect(lambda: init_add_product())
        self.pb_refresh_inventory.clicked.connect(lambda: refresh_page(self))
