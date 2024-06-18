"""Interact with FitTrackee API."""

import requests


class FitTrackee:
    url = ""
    token = None
    token_header = None
    user = None

    def __init__(self):
        """Initialise the class."""

    def setUrl(self, url: str) -> None:
        """Set url and ensure it is correctly formatted.

        Parameters
        ----------
        url : str
           URL of the server.
        """
        if url.endswith("/"):
            self.url = url
        else:
            self.url = url + "/"

    def setToken(self, token):
        """Set the Token."""
        self.token = token
        self.token_header = {"Authorization": f"Bearer {self.token}"}

    def login(self, url: str, email: str, password: str) -> None:
        """Login/authenticate with the server.

        Parameters
        ----------
        url : str
            URL of target server.
        email : str
            Email address of registered user.
        password : str
            Password for 'email'.
        """
        # Authenticate
        self.setUrl(url)
        url = self.url + "api/auth/login"
        json = {"email": email, "password": password}
        resp = requests.post(url, json=json)
        if resp.status_code == 200:
            json = resp.json()
            self.token = json["auth_token"]
            self.setToken(self.token)
            # Get User Info
            return self.getUserInfo()
        return False

    def getUserInfo(self):
        url = self.url + "api/auth/profile"
        resp = requests.get(url, headers=self.token_header)
        if resp.status_code == 200:
            json = resp.json()
            self.user = json["data"]["username"]
            return True
        return False

    def add_workout(self, gpx, sport_id=0, equipment_id="", title=None, notes=""):
        url = self.url + "api/workouts"
        data = {"sport_id": sport_id, "notes": notes}
        if equipment_id != "":
            data["equipment_ids"] = [equipment_id]
        file = {"file": ("workout.gpx", gpx), "data": (None, str(data).replace("'", '"'))}
        resp = requests.post(url, headers=self.token_header, files=file)
        if resp.status_code == 201:
            json = resp.json()
            workout_id = json["data"]["workouts"][0]["id"]
            if title is not None and title != "":
                # Rename Workout to set Title
                url = self.url + "api/workouts/" + workout_id
                data = {"title": title}
                resp = requests.patch(url, headers=self.token_header, json=data)
            return True
        print(resp.json())
        return False

    def add_workout_no_gpx(self, date, duration, distance, sport_id=0, title=None, notes="", ascent=None, descent=None):
        url = self.url + "api/workouts/no_gpx"
        data = {
            "sport_id": sport_id,
            "workout_date": date,
            "duration": duration,
            "distance": distance,
            "ascent": ascent,
            "descent": descent,
            "notes": notes,
            "title": title,
        }
        resp = requests.post(url, headers=self.token_header, json=data)
        if resp.status_code == 201:
            return True
        print(resp.json())
        return False

    def get_sports(self, only_active=False):
        url = self.url + "api/sports"
        resp = requests.get(url, headers=self.token_header)
        if resp.status_code == 200:
            json = resp.json()
            if only_active:
                sports = []
                for sport in json["data"]["sports"]:
                    if sport["is_active_for_user"]:
                        sports.append(sport)
            else:
                sports = json["data"]["sports"]
            return sports
        return None

    def get_equipment(self, only_active=False):
        url = self.url + "api/equipments"
        resp = requests.get(url, headers=self.token_header)
        if resp.status_code == 200:
            json = resp.json()
            if only_active:
                equipment = []
                for item in json["data"]["equipments"]:
                    if item["is_active"]:
                        equipment.append(item)
            else:
                equipment = json["data"]["equipments"]
            return equipment
        return None
