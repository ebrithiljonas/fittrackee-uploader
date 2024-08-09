"""Module for loading .fit file types."""

import datetime
from pathlib import Path

import fitdecode
import workout.workout as workout

# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes


class FitFile(workout.Workout):
    """
    Class for loading .fit files.

    Parameters
    ----------
    path : str | Path
        Path to '.fit' workout file.
    """

    time = (None,)
    distance: float = (None,)
    date = (None,)
    ascent: float = (None,)
    descent = (None,)

    def __init__(self, path: str | Path) -> None:
        """
        Initialise the class.

        Parameters
        ----------
        path : str | Path
            Path to '.fit' workout file.
        """
        # Read Fit File
        self.path = path
        self.file = fitdecode.FitReader(path)
        # Get Information
        self.attributes = {}
        self.records = []
        for frame in self.file:
            if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                # Get Custom Sport Type
                if frame.name == "sport":
                    for field in frame.fields:
                        if field.name == "name":
                            self.attributes["custom_sport"] = field.raw_value
                # Get Properties from Session
                elif frame.name == "session":
                    if frame.has_field("timestamp"):
                        self.date = frame.get_value("timestamp")
                    if frame.has_field("total_distance"):
                        self.distance = frame.get_value("total_distance") / 1000
                    if frame.has_field("total_elapsed_time"):
                        self.time = datetime.timedelta(seconds=int(frame.get_value("total_elapsed_time")))
                    if frame.has_field("total_ascent"):
                        self.ascent = frame.get_value("total_ascent")
                    if frame.has_field("total_ascent"):
                        self.descent = frame.get_value("total_descent")
                    if frame.has_field("enhanced_avg_speed"):
                        self.attributes["avg_speed"] = frame.get_value("enhanced_avg_speed")
                    if frame.has_field("enhanced_max_speed"):
                        self.attributes["max_speed"] = frame.get_value("enhanced_max_speed")
                    if frame.has_field("total_calories"):
                        self.attributes["calories"] = frame.get_value("total_calories")
                    if frame.has_field("max_heart_rate"):
                        self.attributes["max_heart_rate"] = frame.get_value("max_heart_rate")
                    if frame.has_field("avg_heart_rate"):
                        self.attributes["avg_heart_rate"] = frame.get_value("avg_heart_rate")
                    if frame.has_field("sport"):
                        self.attributes["sport"] = frame.get_value("sport")

                if frame.name == "record":
                    self.records.append(Record(frame))
        # Sort Records
        if self.records:
            self.records = sorted(self.records, key=lambda x: x.timestamp)
        points = []
        for record in self.records:
            if record.has_position():
                point = workout.Point(
                    record.timestamp,
                    (record.getLat(), record.getLong()),
                    record.altitude,
                    record.speed,
                    record.heart_rate,
                    record.cadence,
                    record.speed,
                )
                points.append(point)

        super().__init__(
            points, self.path, self.getStats(), self.date, self.time, self.distance, self.ascent, self.descent
        )

    def getSport(self) -> int | None:
        """
        Extract sport based on attributes.

        Returns
        -------
        int | None
            Integer indicating sport type or None.
        """
        sport = self.attributes["sport"]
        if sport == "cycling":
            return 1
        if sport == "running":
            return 5
        return None

    def getStats(self) -> str:
        """
        Extract statistics.

        Returns
        -------
        str
            String of average and maximum heart rate, calories and sport type.
        """
        stats = ""
        if self.attributes is not None:
            stats = f'Average Heart Rate: {self.attributes["avg_heart_rate"]} Bpm \n'
            stats += f'Maximum Heart Rate: {self.attributes["max_heart_rate"]} Bpm \n'
            stats += f'Calories: {self.attributes["calories"]} kcal \n'
            stats += f'Sport Type: {self.attributes["custom_sport"]}'
        return stats


class Record:
    """
    Class for Record.

    Parameters
    ----------
    frame : None
        Frame to be processed.
    """

    timestamp = None
    position_lat: float = None
    position_long: float = None
    distance: float = None
    speed: float = None
    altitude: float = None
    heart_rate: float = None
    cadence: float = None
    temperature: float = None

    def __init__(self, frame: None):
        """
        Initialise the class.

        Parameters
        ----------
        frame : None
            Frame to be processed.
        """
        if frame.has_field("timestamp"):
            self.timestamp = frame.get_value("timestamp")
        if frame.has_field("position_lat"):
            self.position_lat = frame.get_value("position_lat")
        if frame.has_field("position_long"):
            self.position_long = frame.get_value("position_long")
        if frame.has_field("distance"):
            self.distance = frame.get_value("distance")
        if frame.has_field("enhanced_speed"):
            self.speed = frame.get_value("enhanced_speed")
        if frame.has_field("enhanced_altitude"):
            self.altitude = frame.get_value("enhanced_altitude")
        if frame.has_field("heart_rate"):
            self.heart_rate = frame.get_value("heart_rate")
        if frame.has_field("cadence"):
            self.cadence = frame.get_value("cadence")
        if frame.has_field("temperature"):
            self.temperature = frame.get_value("temperature")

    def has_position(self) -> bool:
        """
        Whether a frame has a GPS position.

        Returns
        -------
        bool
            Boolean indicating whether GPS track has latitude/longitude.
        """
        if self.position_lat is not None and self.position_long is not None:
            return True
        return False

    def getLat(self, precision: int) -> float:
        """
        Extract latitude.

        Parameters
        ----------
        precision : int
            Number of decimal points to round latitude to.

        Returns
        -------
        float
            Latitude.
        """
        return round(float(self.position_lat * 180) / float(2**31), ndigits=precision)

    def getLong(self, precision: int):
        """
        Extract longitude.

        Parameters
        ----------
        precision : int
            Number of decimal points to round longitude to.

        Returns
        -------
        float
            Longitude.
        """
        return round(float(self.position_long * 180) / float(2**31), ndigits=precision)
