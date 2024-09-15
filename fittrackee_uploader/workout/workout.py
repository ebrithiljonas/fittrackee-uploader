"""Sub-module for working with a worklout."""

import math
from pathlib import Path

import gpxpy

# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes


class Workout:
    """
    Workout class.

    Parameters
    ----------
    points : None
        GPS points.
    path : str | Path
        Path to file.
    stats : str
        Statistics.
    date : str
        Date of workout.
    time : str
        Time of workout.
    distance : int | float
        Distance of workout.
    ascent : int | float
        Ascent of workout.
    descent : int | float
        Descent of workout.
    """

    def __init__(
        self,
        points: None,
        path: str | Path,
        stats: str = "",
        date: str = None,
        time: str = None,
        distance: int | float = None,
        ascent: int | float = None,
        descent: int | float = None,
    ) -> None:
        """
        Initialise the class.

        Parameters
        ----------
        points : None
            GPS points.
        path : str | Path
            Path to file.
        stats : str
            Statistics.
        date : str
            Date of workout.
        time : str
            Time of workout.
        distance : int | float
            Distance of workout.
        ascent : int | float
            Ascent of workout.
        descent : int | float
            Descent of workout.
        """
        self.points = points
        self.stats = stats
        self.path = path
        self.date = date
        self.time = time
        self.distance = distance
        self.ascent = ascent
        self.descent = descent

    def getExtent(self) -> list[tuple[float, float], tuple[float, float]]:
        """
        Extract bounding box for track.

        Returns
        -------
        tuple
            Minimum and Maximum latitude/longitude which forms a bounding box around GPS points.
        """
        min_lat = self.points[0].getLat()
        max_lat = min_lat
        min_lon = self.points[0].getLong()
        max_lon = min_lon

        for point in self.points:
            lat = point.getLat()
            lon = point.getLong()
            max_lat = max(lat, max_lat)
            min_lat = min(lat, min_lat)
            max_lon = max(lon, max_lon)
            min_lon = min(lon, min_lon)

        return [(min_lat, min_lon), (max_lat, max_lon)]

    def getCenter(self) -> tuple[float, float]:
        """
        Determine the middle of the bounding box for the track.

        Returns
        -------
        tuple[float, float]
            Latitude and Longitude of mid-point of bounding box.
        """
        extent = self.getExtent()
        min_coord = extent[0]
        max_coord = extent[1]
        center_lat = ((max_coord[0] - min_coord[0]) / 2) + min_coord[0]
        center_lon = ((max_coord[1] - min_coord[1]) / 2) + min_coord[1]
        return (center_lat, center_lon)

    def getPath(self) -> list[float]:
        """
        Extract the GPS points.

        Returns
        -------
        list
            List of GPS latitude and longitude.
        """
        path = []
        for point in self.points:
            path.append(point.position)
        return path

    def getGPX(self, precision: int = 3) -> str:
        """
        Extract GPX data.

        Extracts latitude, longitude, altitude, timestamp and speed from GPX returning as XML.

        Parameters
        ----------
        precision : int
            Decimal places to round altitude to.

        Returns
        -------
        str
            XML version of GPX track.
        """
        gpx = gpxpy.gpx.GPX()
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        # Create points:
        for point in self.points:
            point = gpxpy.gpx.GPXTrackPoint(
                point.getLat(), point.getLong(), round(point.altitude, precision), point.timestamp, speed=point.speed
            )
            gpx_segment.points.append(point)
        return gpx.to_xml(version="1.0")

    def getStats(self) -> dict:
        """
        Get statistics.

        Returns
        -------
        dict
            Statistics from GPX track.
        """
        return self.stats

    def getFilePath(self) -> str | Path:
        """
        Get file path.

        Returns
        -------
        str | Path
            Path to GPX file.
        """
        return self.path

    def getDate(self) -> str:
        """
        Get date.

        Returns
        -------
        str
            Date of activity.
        """
        if self.date is None:
            return self.points[0].timestamp
        return self.date

    def getTime(self) -> float:
        """
        Get time.

        Returns
        -------
        float
            Time of activity.
        """
        if self.time is None:
            return self.points[-1].timestamp - self.points[0].timestamp
        return self.time

    def getDistance(self) -> float:
        """
        Get distance.

        Returns
        -------
        float
            Distance.
        """
        if self.distance is None:
            distance = 0.0
            for i in range(len(self.points) - 1):
                distance += self._distance(self.points[i].position, self.points[i + 1].position)
            return distance
        return self.distance

    def _distance(self, origin: tuple, destination: tuple) -> float:
        """
        Calculate distance in kilometres between two points.

        Uses the `Great-circle distance https://en.wikipedia.org/wiki/Great-circle_distance` method to calculate the
        distance between two points on the surface of a sphere, in this case the Earth's  surface.

        Parameters
        ----------
        origin : tuple
            Starting latitude/longitude.
        destination : tuple
            Finishing latitude/longitude.

        Returns
        -------
        float
            Distance between two points in km.
        """
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)
        ) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d


class Point:
    """
    Class for points.

    Parameters
    ----------
    timestamp : str | datetime
        Timestamp for GPS point.
    position : tuple
        Latitude and longitude of the point.
    altitude : float
        Altitude of the point.
    speed : float
        Speed (from GPS device).
    heart_rate : float
        Heart-rate from device.
    cadence : float
        Cadence from device.
    temperature : float
        Temperature from device.
    """

    def __init__(
        self,
        timestamp: str,
        position: tuple,
        altitude: float = None,
        speed: float = None,
        heart_rate: float = None,
        cadence: float = None,
        temperature: float = None,
    ):
        """
        Initialise the class.

        Parameters
        ----------
        timestamp : str | datetime
            Timestamp for GPS point.
        position : tuple
            Latitude and longitude of the point.
        altitude : float
            Altitude of the point.
        speed : float
            Speed (from GPS device).
        heart_rate : float
            Heart-rate from device.
        cadence : float
            Cadence from device.
        temperature : float
            Temperature from device.
        """
        self.timestamp = timestamp
        self.position = position
        self.altitude = altitude
        self.speed = speed
        self.heart_rate = heart_rate
        self.cadence = cadence
        self.temperature = temperature

    def getLat(self):
        """
        Get Latitude.

        Returns
        -------
        float
            Longitude.
        """
        return self.position[0]

    def getLong(self) -> float:
        """
        Get Longitude.

        Returns
        -------
        float
            Longitude.
        """
        return self.position[1]
