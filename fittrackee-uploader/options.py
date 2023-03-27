from PyQt6 import QtWidgets
from ui.options import Ui_OptionsWindow

class Options(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_OptionsWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()

    def setup_callbacks(self):
        # TODO Setup Callbacks
        pass

    # TODO Load / Save Settings
    # TODO Open File Dialogs