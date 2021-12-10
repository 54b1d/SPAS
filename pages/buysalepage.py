from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from spas_functions import init_inv_transaction, init_add_product


class BuySale(QWidget):
    # Class name is important as its imported
    # to __main__ as it is

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/buySale.ui', self)
        self.pb_buy.clicked.connect(lambda: init_inv_transaction("BUY"))
        self.pb_sale.clicked.connect(lambda: init_inv_transaction("SALE"))
        self.pb_add_new_product.clicked.connect(lambda: init_add_product())
