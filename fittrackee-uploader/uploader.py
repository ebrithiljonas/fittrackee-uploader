import sys
import io
import folium
from PyQt6 import QtWidgets

import fit
from ui.main import Ui_MainWindow
import options
import login

class Uploader(QtWidgets.QMainWindow):

    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()

        self.options_window = options.Options()
        self.login_window = login.Login()
        
        # TODO Debug Only
        fitfile = fit.FitFile("test.fit")
        self.setMap(fitfile.getWorkout())

        # TODO Load Settings
        # TODO Try Login --> If it fails, show Login Screen
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