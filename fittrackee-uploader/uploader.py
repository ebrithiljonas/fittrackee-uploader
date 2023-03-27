import sys
import io
import folium
from PyQt6 import QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView

import fit
from ui.main import Ui_MainWindow

class Uploader(QtWidgets.QMainWindow):

    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()
        
        fitfile = fit.FitFile("test.fit")
        self.setMap(fitfile.getWorkout())

        self.show()
        sys.exit(app.exec())

    def setup_callbacks(self):
        pass

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



if __name__ == '__main__':
    uploader = Uploader()