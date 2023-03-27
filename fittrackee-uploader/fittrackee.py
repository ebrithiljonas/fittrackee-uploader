import requests

class FitTrackee():

    link = None
    token = None
    token_header = None
    user = None

    def __init__(self, link: str):
        if link.endswith('/'):
            self.link = link
        else:
            self.link = link + '/'

    def login(self, email: str, password: str):
        # Authenticate
        url = self.link + 'api/auth/login'
        json = {'email': email, 'password': password}
        resp = requests.post(url, json = json)
        if resp.status_code == 200:
            json = resp.json()
            self.token = json['auth_token']
            self.token_header = {'Authorization': f'Bearer {self.token}'}
            # Get User Info
            url = self.link + 'api/auth/profile'
            resp = requests.get(url, headers=self.token_header)
            if resp.status_code == 200:
                json = resp.json()
                self.user = json['data']['username']
            else:
                print('Failed to get Userdata')
        else:
            print('Failed to login')

    def add_workout(self, gpx, sport_id=0, title=None, attributes=None):
        url = self.link + 'api/workouts'
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
                url = self.link + "api/workouts/" + workout_id
                data = {'title': title}
                resp = requests.patch(url, headers=self.token_header, json=data)
            return True
        else:
            print(resp.json())
            return False

    def get_sports(self):
        url = self.link + 'api/sports'
        resp = requests.get(url, headers=self.token_header)
        if resp.status_code == 200:
            json = resp.json()
            sports = json['data']['sports']
            return sports
        else:
            return None

# from fit import FitFile

# # ft = FitTrackee('https://workout.ebrithil.ch/')
# # ft.login('asd@ebrithil.ch', 'test1234')
# # print(ft.get_sports())

# f1 = FitFile('/home/jonas/Nextcloud/Fitness/Logs/Joggen/2021-09-05-11-50-47-Jogging-3km.fit')
# f2 = FitFile('/home/jonas/Nextcloud/Fitness/Logs/Joggen/2021-09-06-11-07-22-Jogging-3km.fit')

# pass

# ft.add_workout(f.getGPX(), 2, "Test Title", f.attributes)