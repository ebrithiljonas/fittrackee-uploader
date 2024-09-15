"""GPX sub-module."""

import gpxpy
from .workout import Point, Workout
from typing_extensions import override

# pylint: disable=too-few-public-methods


class GPX(Workout):
    """
    GPX class.

    Parameters
    ----------
    path : str
        Path to GPX file.
    encoding : str
        Encoding of GPX file to be opened.
    """

    def __init__(self, path: str, encoding: str = "utf-8") -> None:
        """
        Initialise class.

        Parameters
        ----------
        path : str
            Path to GPX file.
        encoding : str
            Encoding of GPX file to be opened.
        """
        with open(path, encoding=encoding) as f:
            self.gpx_file = gpxpy.parse(f)
        points = []
        for track in self.gpx_file.tracks:
            for segment in track.segments:
                for p in segment.points:
                    point = Point(p.time, (p.latitude, p.longitude), p.elevation)
                    points.append(point)
        super().__init__(points, path)

    @override
    def getGPX(self, version: str = "1.0") -> None:
        """
        Extract GPX data to XML.

        Parameters
        ----------
        version : str
            GPX version.

        Returns
        -------
        xml
            XML formatted data from GPX file.
        """
        return self.gpx_file.to_xml(version=version)
