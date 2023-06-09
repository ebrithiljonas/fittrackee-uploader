import fitdecode
import datetime
import workout.workout as workout

class FitFile(workout.Workout):

    time = None
    distance = None
    date = None
    ascent = None
    descent = None

    def __init__(self, path):
        # Read Fit File
        self.path = path
        self.file = fitdecode.FitReader(path)
        # Get Information
        self.attributes = {}
        self.records = []
        for frame in self.file:
            if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                # Get Custom Sport Type
                if frame.name == 'sport':
                    for field in frame.fields:
                        if field.name == 'name':
                            self.attributes['custom_sport'] = field.raw_value
                # Get Properties from Session
                elif frame.name == 'session':
                    if frame.has_field('timestamp'):
                        self.date = frame.get_value('timestamp')
                    if frame.has_field('total_distance'):
                        self.distance = frame.get_value('total_distance') / 1000
                    if frame.has_field('total_elapsed_time'):
                        self.time = datetime.timedelta(seconds=int(frame.get_value('total_elapsed_time')))
                    if frame.has_field('total_ascent'):
                        self.ascent = frame.get_value('total_ascent')
                    if frame.has_field('total_ascent'):
                        self.descent = frame.get_value('total_descent')
                    if frame.has_field('enhanced_avg_speed'):
                        self.attributes['avg_speed'] = frame.get_value('enhanced_avg_speed')
                    if frame.has_field('enhanced_max_speed'):
                        self.attributes['max_speed'] = frame.get_value('enhanced_max_speed')
                    if frame.has_field('total_calories'):
                        self.attributes['calories'] = frame.get_value('total_calories')
                    if frame.has_field('max_heart_rate'):
                        self.attributes['max_heart_rate'] = frame.get_value('max_heart_rate')
                    if frame.has_field('avg_heart_rate'):
                        self.attributes['avg_heart_rate'] = frame.get_value('avg_heart_rate')
                    if frame.has_field('sport'):
                        self.attributes['sport'] = frame.get_value('sport')
                
                if frame.name == 'record':
                    self.records.append(Record(frame))
        # Sort Records
        if self.records:
            self.records = sorted(self.records, key=lambda x: x.timestamp)
        points = []
        for record in self.records:
            if record.has_position():
                point = workout.Point(record.timestamp, (record.getLat(), record.getLong()), record.altitude, record.speed, record.heart_rate, record.cadence, record.speed)
                points.append(point)
        
        super().__init__(points, self.path, self.getStats(), self.date, self.time, self.distance, self.ascent, self.descent)

    def getSport(self):
        sport = self.attributes['sport']
        if sport == 'cycling': return 1
        elif sport == 'running': return 5
        else: return None

    def getStats(self):
        if self.attributes is None:
            stats = ''
        else:
            stats = f'Average Heart Rate: {self.attributes["avg_heart_rate"]} Bpm \n'
            stats += f'Maximum Heart Rate: {self.attributes["max_heart_rate"]} Bpm \n'
            stats += f'Calories: {self.attributes["calories"]} kcal \n'
            stats += f'Sport Type: {self.attributes["custom_sport"]}'
        return stats

class Record:

    timestamp = None
    position_lat = None
    position_long = None
    distance = None
    speed = None
    altitude = None
    heart_rate = None
    cadence = None
    temperature = None

    def __init__(self, frame):
        if frame.has_field('timestamp'): self.timestamp = frame.get_value('timestamp')
        if frame.has_field('position_lat'): self.position_lat = frame.get_value('position_lat')
        if frame.has_field('position_long'): self.position_long = frame.get_value('position_long')
        if frame.has_field('distance'): self.distance = frame.get_value('distance')
        if frame.has_field('enhanced_speed'): self.speed = frame.get_value('enhanced_speed')
        if frame.has_field('enhanced_altitude'): self.altitude = frame.get_value('enhanced_altitude')
        if frame.has_field('heart_rate'): self.heart_rate = frame.get_value('heart_rate')
        if frame.has_field('cadence'): self.cadence = frame.get_value('cadence')
        if frame.has_field('temperature'): self.temperature = frame.get_value('temperature')

    def has_position(self):
        if self.position_lat != None and self.position_long != None:
            return True
        else:
            return False

    def getLat(self):
        return round(float(self.position_lat * 180) / float(2**31), 9) 

    def getLong(self):
        return round(float(self.position_long * 180) / float(2**31), 9)