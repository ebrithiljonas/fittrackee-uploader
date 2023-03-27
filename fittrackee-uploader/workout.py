import gpxpy

class Workout:

    def __init__(self, points):
        self.points = points

    def getExtent(self):
        min_lat = self.points[0].getLat()
        max_lat = min_lat
        min_lon = self.points[0].getLong()
        max_lon = min_lon

        for point in self.points:
            lat = point.getLat()
            lon = point.getLong()
            if lat > max_lat:
                max_lat = lat
            if lat < min_lat:
                min_lat = lat
            if lon > max_lon:
                max_lon = lon
            if lon < min_lon:
                min_lon = lon

        return [(min_lat, min_lon), (max_lat, max_lon)]

    def getCenter(self):
        extent = self.getExtent()
        min_coord = extent[0]
        max_coord = extent[1]
        center_lat = ((max_coord[0] - min_coord[0]) / 2) + min_coord[0]
        center_lon = ((max_coord[1] - min_coord[1]) / 2) + min_coord[1]
        return (center_lat, center_lon)

    def getPath(self):
        path = []
        for point in self.points:
            path.append(point.position)
        return path

    def getGPX(self):
        gpx = gpxpy.gpx.GPX()
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        # Create points:
        for point in self.points:
            if point.has_position():
                point = gpxpy.gpx.GPXTrackPoint(point.getLat(), point.getLong(), round(point.altitude, 3), point.timestamp, speed=point.speed)
                gpx_segment.points.append(point)
        return gpxpy.gpx.to_xml(version='1.0')

class Point:

    def __init__(self, timestamp, position, altitude=None, speed=None, heart_rate=None, cadence=None, temperature=None):
        self.timestamp = timestamp
        self.position = position
        self.altitude = altitude
        self.speed = speed
        self.heart_rate = heart_rate
        self.cadence = cadence
        self.temperature = temperature

    def getLat(self):
        return self.position[0]

    def getLong(self):
        return self.position[1]