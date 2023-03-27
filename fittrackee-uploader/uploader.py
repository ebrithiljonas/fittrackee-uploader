import sys
import io
import folium
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

import fit

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

"""
Folium in PyQt5
"""
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

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

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')