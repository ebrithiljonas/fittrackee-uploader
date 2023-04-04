import sys
import io
import os
import folium
import webbrowser
from PyQt6 import QtWidgets

import fittrackee
from ui.main import Ui_MainWindow
import options
import login
import configuration
import workout.workout as workout
import workout.loader as loader
import templates

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

        self.options_window = options.Options(self, self.config)
        self.login_window = login.Login(self, self.config, self.api)

        self.login()

        self.files = []
        self.loader = loader.Loader()
        self.current_workout = None

        if self.config.folder != '':
            self.loadFolder()

        self.show()
        sys.exit(app.exec())

    def login(self):
        if '' in [self.config.server_url, self.config.email, self.config.token]:
            self.showWindowonCenter(self.login_window)
        else:
            # Try saved token
            self.api.setUrl(self.config.server_url)
            self.api.setToken(self.config.token)
            if not self.api.getUserInfo():
                self.showWindowonCenter(self.login_window)
            else:
                self.loadSports()
                self.ui.labelLoginStats.setText(f'Logged in as {self.api.user} on {self.api.url}')
                self.ui.btUpload.setEnabled(True)

    def logout(self):
        self.ui.btUpload.setEnabled(False)
        self.config.token = ''
        self.config.saveConfig()
        self.ui.labelLoginStats.setText('')
        self.ui.cbSportType.clear()
        self.login()

    def setup_callbacks(self):
        self.ui.actionQuit.triggered.connect(sys.exit)
        self.ui.actionReload.triggered.connect(self.loadFolder)
        self.ui.actionOptions.triggered.connect(self.options)
        self.ui.actionLogout.triggered.connect(self.logout)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.btUpload.clicked.connect(self.upload)

    def about(self):
        webbrowser.open('https://github.com/ebrithiljonas/fittrackee-uploader')

    def loadFolder(self, path=None):
        if path is None or path == False:
            path = self.config.folder
        if os.path.isdir(path):
            self.files.clear()
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
                if os.path.isfile(file_path):
                    self.files.append(file_path)
            self.loadNextFile()

    def loadFile(self, path):
        if os.path.isfile(path):
            self.current_workout = self.loader.loadFile(path)
            if not self.current_workout is None:
                self.setMap(self.current_workout)
                self.ui.statusbar.showMessage(path)
                stats = f'{self.current_workout.getDate().strftime("%d %b, %Y")}   {self.current_workout.getTime()}   {self.current_workout.getDistance():.2f} km'
                self.ui.labelStats.setText(stats)

    def loadNextFile(self):
        if len(self.files) > 0:
            file_path = self.files.pop(0)
            self.loadFile(file_path)
        else:
            self.setMap(None)
            self.ui.statusbar.clearMessage()
            self.ui.labelStats.setText('')
            pass

    def setMap(self, wo):

        if wo is None:
            self.ui.btUpload.setEnabled(False)
            self.ui.webMap.setHtml(templates.page_no_more_files)
        elif len(wo.points) == 0:
            self.ui.btUpload.setEnabled(True)
            self.ui.webMap.setHtml(templates.page_no_gps_records)
        else:
            self.ui.btUpload.setEnabled(True)
            m = folium.Map(
                tiles='OpenStreetMap'
            )

            m.fit_bounds(wo.getExtent())

            path = folium.PolyLine(wo.getPath(), color="#0000FF")
            path.add_to(m)
            
            data = io.BytesIO()
            m.save(data, close_file=False)

            self.ui.webMap.setHtml(data.getvalue().decode())

    def loadSports(self):
        self.sports = self.api.get_sports(True)
        self.ui.cbSportType.clear()
        for sport in self.sports:
                self.ui.cbSportType.addItem(sport['label'])

    def getSportID(self, sport_name):
        if len(self.sports) > 0:
            for sport in self.sports:
                if sport['label'] == sport_name:
                    return sport['id']
        return -1

    def upload(self):
        gpx = self.current_workout.getGPX()
        sport_id = self.getSportID(self.ui.cbSportType.currentText())
        title = self.ui.tbTitle.text()
        notes = self.current_workout.getStats()
        if self.api.add_workout(gpx, sport_id, title, notes):
            self.ui.tbTitle.setText('')
            if self.config.move_after_upload:
                if os.path.isdir(self.config.uploaded_folder):
                    file_name = os.path.basename(self.current_workout.getFilePath())
                    if self.config.add_info_to_file_name:
                        sport_name = self.ui.cbSportType.currentText()
                        sport_name = sport_name.split('(')[0]
                        sport_name = sport_name.lower().replace(' ', '')
                        new_file_name = f'{os.path.splitext(file_name)[0]}_{sport_name}_{title}{os.path.splitext(file_name)[1]}'
                    else:
                        new_file_name = file_name
                    new_file_path = os.path.join(self.config.uploaded_folder, new_file_name)
                    os.rename(self.current_workout.getFilePath(), new_file_path)
            self.loadNextFile()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setText("Upload Failed")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.exec()

    def showWindowonCenter(self, window):
        window.show()
        #  TODO Figure this Garbage out (atm, issues with multi monitors)
        # pos = QtCore.QPoint()
        # pos.setX(int(window.pos().x() + (self.frameGeometry().width() / 2)))
        # pos.setY(int(window.pos().y() + (self.frameGeometry().height() / 2)))
        # window.move(pos)
        window.activateWindow()

    def options(self):
        self.showWindowonCenter(self.options_window)
        
if __name__ == '__main__':
    uploader = Uploader()