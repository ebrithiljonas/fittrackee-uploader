"""Module for loading GPX."""

import os

import workout.fit as fit
import workout.gpx as gpx

# pylint: disable=too-few-public-methods


class Loader:
    """Class for loading GPX."""

    filetypes: dict = {
        ".fit": fit.FitFile,
        ".gpx": gpx.GPX,
    }

    def __init__(self):
        """Initialise the class."""

    def loadFile(self, path: str) -> str | None:
        """
        Load a file using appropriate method.

        Parameters
        ----------
        path : str
            Path to file.

        Returns
        -------
        str | None
            Path to files or None.
        """
        if os.path.isfile(path):
            extension = os.path.splitext(path)[1]
            if extension in self.filetypes:
                return self.filetypes[extension](path)
        return None
