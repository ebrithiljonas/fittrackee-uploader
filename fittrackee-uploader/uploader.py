import sys
import io
import folium
from PyQt6 import QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView

import fit
from ui.main import Ui_MainWindow

# ===== Move to seperate class =====

def calculate_extent(coords):
    min_lon = min(coords, key=lambda tup: tup[1])[1]
    max_lon = max(coords, key=lambda tup: tup[1])[1]
    min_lat = min(coords, key=lambda tup: tup[0])[0]
    max_lat = max(coords, key=lambda tup: tup[0])[0]

    return [(min_lat, min_lon), (max_lat, max_lon)]

def calculate_center(coords):
    extent = calculate_extent(coords)
    min_coord = extent[0]
    max_coord = extent[1]
    center_lat = ((max_coord[0] - min_coord[0]) / 2) + min_coord[0]
    center_lon = ((max_coord[1] - min_coord[1]) / 2) + min_coord[1]
    return (center_lat, center_lon)

# ========================================

class Uploader(QtWidgets.QMainWindow):

    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_callbacks()
        
        fitfile = fit.FitFile("test.fit")
        self.setMap(fitfile.getPoints())

        self.show()
        sys.exit(app.exec())

    def setup_callbacks(self):
        pass

    def setMap(self, path):
        m = folium.Map(
        	tiles='OpenStreetMap'
        )

        # TODO Replace calculate_extent with Path Object
        m.fit_bounds(calculate_extent(path))
        path = folium.PolyLine(path, color="#0000FF")
        path.add_to(m)
        
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.ui.webMap.setHtml(data.getvalue().decode())



if __name__ == '__main__':
    uploader = Uploader()