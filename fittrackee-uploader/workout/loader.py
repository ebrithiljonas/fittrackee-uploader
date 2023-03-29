import os
import workout.workout as workout
import workout.fit as fit
import workout.gpx as gpx

class Loader:

    filetypes = {
        ".fit": fit.FitFile,
        ".gpx": gpx.GPX,
    }

    def __init__(self):
        pass

    def loadFile(self, path: str):
        if os.path.isfile(path):
            extension = os.path.splitext(path)[1]
            if extension in self.filetypes:
                return self.filetypes[extension](path)
            else:
                return None