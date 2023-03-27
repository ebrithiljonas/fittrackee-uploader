import requests

class FitTrackee():

    url = None
    token = None
    token_header = None
    user = None

    def __init__(self):
        pass

    def setUrl(self, url):
        if url.endswith('/'):
            self.url = url
        else:
            self.url = url + '/'

    def setToken(self, token):
        self.token = token
        self.token_header = {'Authorization': f'Bearer {self.token}'}

    def login(self,url: str, email: str, password: str):
        # Authenticate
        self.setUrl(url)
        url = self.url + 'api/auth/login'
        json = {'email': email, 'password': password}
        resp = requests.post(url, json = json)
        if resp.status_code == 200:
            json = resp.json()
            self.token = json['auth_token']
            self.setToken(self.token)
            # Get User Info
            return self.getUserInfo()
        else:
            return False

    def getUserInfo(self):
        url = self.url + 'api/auth/profile'
        resp = requests.get(url, headers=self.token_header)
        if resp.status_code == 200:
            json = resp.json()
            self.user = json['data']['username']
            return True
        else:
            return False


    def add_workout(self, gpx, sport_id=0, title=None, attributes=None):
        url = self.url + 'api/workouts'
        if attributes is None:
            notes = ''
        else:
            notes = f'Average Heart Rate: {attributes["avg_heart_rate"]} Bpm \n'
            notes += f'Maximum Heart Rate: {attributes["max_heart_rate"]} Bpm \n'
            notes += f'Calories: {attributes["calories"]} kcal \n'
            notes += f'Sport Type: {attributes["custom_sport"]}'
        data = {'sport_id': sport_id, 'notes': notes}
        file = {'file': ('workout.gpx', gpx), 'data': (None, str(data).replace("'",'"'))}
        resp = requests.post(url, headers=self.token_header, files = file)
        if resp.status_code == 201:
            json = resp.json()
            workout_id = json['data']['workouts'][0]['id']
            if title is not None and title != '':
                # Rename Workout to set Title
                url = self.url + "api/workouts/" + workout_id
                data = {'title': title}
                resp = requests.patch(url, headers=self.token_header, json=data)
            return True
        else:
            print(resp.json())
            return False

    def get_sports(self):
        url = self.url + 'api/sports'
        resp = requests.get(url, headers=self.token_header)
        if resp.status_code == 200:
            json = resp.json()
            sports = json['data']['sports']
            return sports
        else:
            return None