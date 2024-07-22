"""Uploader Module."""

import io
import os
import sys
import webbrowser

import configuration
import fittrackee
import folium
import login
import options
import templates
import workout.loader as loader
from PyQt6 import QtCore, QtWidgets
from ui.main import Ui_MainWindow


class Uploader(QtWidgets.QMainWindow):
    """Uploader class."""

    def __init__(self):
        """Initialise the class."""
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
        self.sports = None
        self.equipment = None
        self.current_workout = None

        self.completer_model = QtCore.QStringListModel(self.config.used_names)
        self.completer = QtWidgets.QCompleter(self.completer_model, self)
        self.ui.tbTitle.setCompleter(self.completer)
        if self.config.folder != "":
            self.loadFolder()

        self.show()
        sys.exit(app.exec())

    def login(self) -> None:
        """Login."""
        if "" in [self.config.server_url, self.config.email, self.config.token]:
            self.showWindowonCenter(self.login_window)
        else:
            # Try saved token
            self.api.setUrl(self.config.server_url)
            self.api.setToken(self.config.token)
            if not self.api.getUserInfo():
                self.showWindowonCenter(self.login_window)
            else:
                self.loadSports()
                self.loadEquipment()
                self.ui.labelLoginStats.setText(f"Logged in as {self.api.user} on {self.api.url}")
                self.ui.btUpload.setEnabled(True)

    def logout(self) -> None:
        """Logout."""
        self.ui.btUpload.setEnabled(False)
        self.config.token = ""
        self.config.saveConfig()
        self.ui.labelLoginStats.setText("")
        self.ui.cbSportType.clear()
        self.ui.cbEquipment.clear()
        self.login()

    def setup_callbacks(self) -> None:
        """Callbacks."""
        self.ui.actionQuit.triggered.connect(sys.exit)
        self.ui.actionReload.triggered.connect(self.loadFolder)
        self.ui.actionOptions.triggered.connect(self.options)
        self.ui.actionLogout.triggered.connect(self.logout)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.btUpload.clicked.connect(self.upload)
        self.ui.btSkip.clicked.connect(self.skipFile)

    def about(self) -> None:
        """Open About page in browser."""
        webbrowser.open("https://github.com/ebrithiljonas/fittrackee-uploader")

    def loadFolder(self, path=None) -> None:
        """
        Load folder.

        Parameters
        ----------
        path : str
            Path to load.
        """
        if path is None or path is False:
            path = self.config.folder
        if os.path.isdir(path):
            self.files.clear()
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
                if os.path.isfile(file_path):
                    self.files.append(file_path)
            self.loadNextFile()

    def loadFile(self, path) -> None:
        """
        Load file.

        Parameters
        ----------
        path : str
            File to load.
        """
        if os.path.isfile(path):
            try:
                self.current_workout = self.loader.loadFile(path)
            except:
                self.current_workout = None
                self.ui.labelStats.setText("")
                self.ui.btUpload.setEnabled(False)
                if self.config.auto_skip:
                    self.skipFile()
                else:
                    self.ui.webMap.setHtml(templates.page_failed_to_load)
            self.ui.statusbar.showMessage(path)
            if self.current_workout is not None:
                self.setMap(self.current_workout)
                stats = f'{self.current_workout.getDate().strftime("%d %b, %Y")} {self.current_workout.getTime()} {self.current_workout.getDistance():.2f} km'
                self.ui.labelStats.setText(stats)

    def loadNextFile(self) -> None:
        """Load the next file."""
        if len(self.files) > 0:
            file_path = self.files.pop(0)
            self.loadFile(file_path)
        else:
            self.setMap(None)
            self.ui.statusbar.clearMessage()
            self.ui.labelStats.setText("")

    def setMap(self, wo) -> None:
        """
        Set the map.

        Parameters
        ----------
        wo :
            Workout to set the map for.
        """
        if wo is None:
            self.ui.btUpload.setEnabled(False)
            self.ui.webMap.setHtml(templates.page_no_more_files)
        elif len(wo.points) == 0:
            self.ui.btUpload.setEnabled(True)
            self.ui.webMap.setHtml(templates.page_no_gps_records)
        else:
            self.ui.btUpload.setEnabled(True)
            m = folium.Map(tiles="OpenStreetMap")

            m.fit_bounds(wo.getExtent())

            path = folium.PolyLine(wo.getPath(), color="#0000FF")
            path.add_to(m)

            startPoint = folium.CircleMarker(
                location=wo.points[0].position,
                radius=6,
                color="green",
                stroke=False,
                fill=True,
                fill_opacity=1,
                opacity=1,
                tooltip="Start",
            )
            startPoint.add_to(m)

            finishPoint = folium.CircleMarker(
                location=wo.points[-1].position,
                radius=6,
                color="red",
                stroke=False,
                fill=True,
                fill_opacity=1,
                opacity=1,
                tooltip="Finish",
            )
            finishPoint.add_to(m)

            data = io.BytesIO()
            m.save(data, close_file=False)

            self.ui.webMap.setHtml(data.getvalue().decode())

    def loadSports(self) -> None:
        """Load sports."""
        self.sports = self.api.get_sports(True)
        self.ui.cbSportType.clear()
        if self.sports is not None:
            for sport in self.sports:
                self.ui.cbSportType.addItem(sport["label"])

    def loadEquipment(self) -> None:
        """Load equipment."""
        self.equipment = self.api.get_equipment(True)
        self.ui.cbEquipment.clear()
        self.ui.cbEquipment.addItem("No Equipment")
        if self.equipment is not None:
            for item in self.equipment:
                self.ui.cbEquipment.addItem(item["label"])

    def getSportID(self, sport_name: str) -> int:
        """
        Get sport ID.

        Parameters
        ----------
        sport_name : str
            Sport name.

        Returns
        -------
        int
            Integer code for sport id.
        """
        if len(self.sports) > 0:
            for sport in self.sports:
                if sport["label"] == sport_name:
                    return sport["id"]
        return -1

    def getEquipmentID(self, equipment_name: str) -> int:
        """
        Get equipment ID.

        Parameters
        ----------
        equipment_name : str
            Equipment.

        Returns
        -------
        int
            Integer code for equipment id.
        """
        if equipment_name == "No Equipment":
            return ""
        if len(self.equipment) > 0:
            for item in self.equipment:
                if item["label"] == equipment_name:
                    return item["id"]
        return ""

    def upload(self) -> None:
        """Upload track."""
        result = None
        sport_id = self.getSportID(self.ui.cbSportType.currentText())
        equipment_id = self.getEquipmentID(self.ui.cbEquipment.currentText())
        title = self.ui.tbTitle.text()
        self.config.used_names.add(title)
        self.completer_model.setStringList(self.config.used_names)
        self.config.saveConfig()
        if self.config.add_stats:
            notes = self.current_workout.getStats()
        else:
            notes = ""

        if len(self.current_workout.points) == 0:
            date = self.current_workout.getDate().strftime("%Y-%m-%d %H:%M")
            duration = self.current_workout.getTime().total_seconds()
            distance = self.current_workout.getDistance()
            ascent = self.current_workout.ascent
            descent = self.current_workout.descent
            result = self.api.add_workout_no_gpx(date, duration, distance, sport_id, title, notes, ascent, descent)
        else:
            gpx = self.current_workout.getGPX()
            result = self.api.add_workout(gpx, sport_id, equipment_id, title, notes)

        if result:
            self.ui.tbTitle.setText("")
            if self.config.move_after_upload:
                if os.path.isdir(self.config.uploaded_folder):
                    file_name = os.path.basename(self.current_workout.getFilePath())
                    if self.config.add_info_to_file_name:
                        sport_name = self.ui.cbSportType.currentText()
                        sport_name = sport_name.split("(")[0]
                        sport_name = sport_name.lower().replace(" ", "")
                        new_file_name = (
                            f"{os.path.splitext(file_name)[0]}_{sport_name}_{title}{os.path.splitext(file_name)[1]}"
                        )
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

    def skipFile(self) -> None:
        """Skip file."""
        self.loadNextFile()

    def showWindowonCenter(self, window) -> None:
        """
        Center window.

        Parameters
        ----------
        window
            Window to center.
        """
        window.show()
        #  TODO Figure this Garbage out (atm, issues with multi monitors)
        # pos = QtCore.QPoint()
        # pos.setX(int(window.pos().x() + (self.frameGeometry().width() / 2)))
        # pos.setY(int(window.pos().y() + (self.frameGeometry().height() / 2)))
        # window.move(pos)
        window.activateWindow()

    def options(self) -> None:
        """Show options."""
        self.showWindowonCenter(self.options_window)


if __name__ == "__main__":
    uploader = Uploader()
