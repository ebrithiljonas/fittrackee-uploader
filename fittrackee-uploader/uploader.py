import sys
import io
import folium
from PyQt6 import QtWidgets

import fit
import fittrackee
from ui.main import Ui_MainWindow
import options
import login
import configuration

class Uploader(QtWidgets.QMainWindow):

    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()

        self.config = configuration.Configuration()
        self.config.saveConfig()

        self.api = fittrackee.FitTrackee()

        self.options_window = options.Options(self.config)
        self.login_window = login.Login(self.config, self.api)

        if None in [self.config.server_url, self.config.email, self.config.token]:
            self.login_window.show()
        else:
            # Try saved token
            self.api.setUrl(self.config.server_url)
            self.api.setToken(self.config.token)
            if not self.api.getUserInfo():
                self.login_window.show()

        # TODO If Path is set, load first file

        self.show()
        sys.exit(app.exec())

    def setup_callbacks(self):
        self.ui.actionQuit.triggered.connect(sys.exit)
        self.ui.actionOptions.triggered.connect(self.options)

    def setMap(self, workout):
        m = folium.Map(
        	tiles='OpenStreetMap'
        )

        m.fit_bounds(workout.getExtent())

        path = folium.PolyLine(workout.getPath(), color="#0000FF")
        path.add_to(m)
        
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.ui.webMap.setHtml(data.getvalue().decode())

    def options(self):
        self.options_window.show()
        
if __name__ == '__main__':
    uploader = Uploader()