import os
import workout.workout as workout
import workout.fit as fit

class Loader:

    def __init__(self):
        pass

    def loadFile(self, path: str):
        if os.path.isfile(path):
            if path.endswith('.fit'):
                fit_file = fit.FitFile(path)
                return fit_file.getWorkout()
            elif path.endswith('.gpx'):
                return None
            else:
                return None