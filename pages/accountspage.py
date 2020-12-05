from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from spas_functions import init_add_account, fetch_accounts


class AccountsPage(QWidget):
    # Class name is important as its imported
    # to __main__ as it is

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/accounts.ui', self)
        fetch_accounts(self.table_accounts)
        self.pb_refresh_accounts.clicked.connect(lambda: fetch_accounts(self.table_accounts))
        self.pb_add_account.clicked.connect(lambda: init_add_account(self.table_accounts))
