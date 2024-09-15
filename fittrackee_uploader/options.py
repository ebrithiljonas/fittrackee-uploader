"""Options."""

from PyQt6 import QtWidgets
from .ui.options import Ui_OptionsWindow


class Options(QtWidgets.QWidget):
    """
    Options class.

    Parameters
    ----------
    main_window : None
        Main window.
    configuration : dict
        Configuration options.
    """

    def __init__(self, main_window: None, configuration: dict) -> None:
        """
        Initialise class.

        Parameters
        ----------
        main_window : None
            Main window.
        configuration : dict
            Configuration options.
        """
        super().__init__()
        self.ui = Ui_OptionsWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()

        self.main_window = main_window
        self.configuration = configuration
        self.loadConfig()

    def loadConfig(self):
        """Load configuration."""
        self.ui.tbServer.setText(self.configuration.server_url)
        self.ui.tbFolder.setText(self.configuration.folder)
        self.ui.tbUploadedFolder.setText(self.configuration.uploaded_folder)
        self.ui.cbMoveFiles.setChecked(self.configuration.move_after_upload)
        self.ui.cbAddInfoFile.setChecked(self.configuration.add_info_to_file_name)
        self.ui.cbAddStats.setChecked(self.configuration.add_stats)
        self.ui.cbAutoSkip.setChecked(self.configuration.auto_skip)

    def setup_callbacks(self):
        """Callbacks."""
        self.ui.btCancel.clicked.connect(self.close)
        self.ui.btSave.clicked.connect(self.saveConfig)
        self.ui.btBrowseFolder.clicked.connect(lambda: self.selectFolder(self.ui.tbFolder))
        self.ui.btBrowseUploadedFolder.clicked.connect(lambda: self.selectFolder(self.ui.tbUploadedFolder))

    def saveConfig(self):
        """Save configuration."""
        if self.configuration.folder != self.ui.tbFolder.text():
            self.main_window.loadFolder()
        self.configuration.server_url = self.ui.tbServer.text()
        self.configuration.folder = self.ui.tbFolder.text()
        self.configuration.uploaded_folder = self.ui.tbUploadedFolder.text()
        self.configuration.move_after_upload = self.ui.cbMoveFiles.isChecked()
        self.configuration.add_info_to_file_name = self.ui.cbAddInfoFile.isChecked()
        self.configuration.add_stats = self.ui.cbAddStats.isChecked()
        self.configuration.auto_skip = self.ui.cbAutoSkip.isChecked()
        self.configuration.saveConfig()
        self.close()

    def selectFolder(self, textBox: None) -> None:
        """
        Select folder.

        Parameters
        ----------
        textBox : None
            Text box for selecting GPX directory.
        """
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file != "":
            textBox.setText(file)
