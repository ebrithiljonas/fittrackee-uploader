"""Login."""

from PyQt6 import QtWidgets
from .ui.login import Ui_LoginWindow


class Login(QtWidgets.QWidget):
    """
    Login class.

    Parameters
    ----------
    main_window : None
        Main window.
    configuration : dict
        Configuration options.
    api : None
        API options.
    """

    def __init__(self, main_window: None, configuration: dict, api: None) -> None:
        """
        Initialise class.

        Parameters
        ----------
        main_window : None
            Main window.
        configuration : dict
            Configuration options.
        api : None
            API options.
        """
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()

        self.main_window = main_window
        self.configuration = configuration
        self.api = api

        self.ui.tbServer.setText(self.configuration.server_url)
        self.ui.tbEmail.setText(self.configuration.email)

    def setup_callbacks(self):
        """Callbacks."""
        self.ui.btLogin.clicked.connect(self.login)
        self.ui.btCancel.clicked.connect(self.exit)

    def exit(self):
        """Exit cleanly."""
        self.close()
        self.main_window.close()

    def login(self):
        """Login."""
        url = self.ui.tbServer.text()
        email = self.ui.tbEmail.text()
        password = self.ui.tbPassword.text()
        if "" not in [url, email, password]:
            if self.api.login(url, email, password):
                self.configuration.server_url = url
                self.configuration.email = email
                self.configuration.token = self.api.token
                self.configuration.saveConfig()
                self.close()
                self.ui.tbPassword.setText("")
                self.main_window.login()
