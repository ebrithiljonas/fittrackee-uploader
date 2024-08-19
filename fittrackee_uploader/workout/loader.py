"""Module for loading GPX."""

import os

from .fit import FitFile
from .gpx import GPX

# pylint: disable=too-few-public-methods


class Loader:
    """Class for loading GPX."""

    filetypes: dict = {
        ".fit": FitFile,
        ".gpx": GPX,
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
