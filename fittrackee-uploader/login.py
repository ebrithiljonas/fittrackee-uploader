from PyQt6 import QtWidgets
from ui.login import Ui_LoginWindow

class Login(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()

    def setup_callbacks(self):
        # TODO Setup Callbacks
        pass

    # TODO Login