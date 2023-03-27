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
        extent = calculate_extent(fitfile.getPoints())

        m = folium.Map(
        	tiles='OpenStreetMap'
        )
        m.fit_bounds(extent)
        path = folium.PolyLine(fitfile.getPoints(), color="#0000FF")
        path.add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        map_layout = QtWidgets.QVBoxLayout()
        self.ui.map_widget.setLayout(map_layout)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())

        map_layout.addWidget(webView)

        # self.ui.map_widget. = webView

        self.show()
        sys.exit(app.exec())

    def setup_callbacks(self):
        pass


if __name__ == '__main__':
    uploader = Uploader()