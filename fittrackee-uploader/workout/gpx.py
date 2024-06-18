import gpxpy
import workout.workout as workout
from typing_extensions import override


class GPX(workout.Workout):

    def __init__(self, path):
        with open(path) as f:
            self.gpx_file = gpxpy.parse(f)
        points = []
        for track in self.gpx_file.tracks:
            for segment in track.segments:
                for p in segment.points:
                    point = workout.Point(p.time, (p.latitude, p.longitude), p.elevation)
                    points.append(point)
        super().__init__(points, path)

    @override
    def getGPX(self):
        return self.gpx_file.to_xml(version="1.0")
