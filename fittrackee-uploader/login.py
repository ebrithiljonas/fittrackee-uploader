from PyQt6 import QtWidgets
from ui.login import Ui_LoginWindow

class Login(QtWidgets.QWidget):

    def __init__(self, configuration, api):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()

        self.configuration = configuration
        self.api = api

        self.ui.tbServer.setText(self.configuration.server_url)
        self.ui.tbEmail.setText(self.configuration.email)

    def setup_callbacks(self):
        self.ui.btLogin.clicked.connect(self.login)
        self.ui.btCancel.clicked.connect(self.close)

    def login(self):
        url = self.ui.tbServer.text()
        email = self.ui.tbEmail.text()
        password = self.ui.tbPassword.text()
        if not '' in [url, email, password]:
            if self.api.login(url, email, password):
                self.configuration.server_url = url
                self.configuration.email = email
                self.configuration.token = self.api.token
                self.configuration.saveConfig()
                self.close()