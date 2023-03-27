from PyQt6 import QtWidgets
from ui.options import Ui_OptionsWindow

class Options(QtWidgets.QWidget):

    def __init__(self, configuration):
        super().__init__()
        self.ui = Ui_OptionsWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()
        
        self.configuration = configuration

        self.ui.tbServer.setText(self.configuration.server_url)
        self.ui.tbFolder.setText(self.configuration.folder)
        self.ui.tbUploadedFolder.setText(self.configuration.uploaded_folder)
        self.ui.cbMoveFiles.setChecked(self.configuration.move_after_upload)
        self.ui.cbAddStats.setChecked(self.configuration.add_stats)

    def setup_callbacks(self):
        self.ui.btCancel.clicked.connect(self.close)
        self.ui.btCancel.clicked.connect(self.saveConfig)
        # TODO Setup Callbacks for file openers

    def saveConfig(self):
        self.configuration.server_url = self.ui.tbServer.text()
        self.configuration.folder = self.ui.tbFolder.text()
        self.configuration.uploaded_folder = self.ui.tbUploadedFolder.text()
        self.configuration.move_after_upload = self.ui.cbMoveFiles.isChecked()
        self.configuration.add_stats = self.ui.cbAddStats.isChecked()
        self.configuration.saveConfig()
        self.close()

    # TODO Open File Dialogs