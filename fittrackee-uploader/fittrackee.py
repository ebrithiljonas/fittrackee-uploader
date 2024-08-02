"""Interact with FitTrackee API."""

from pathlib import Path
import requests


class FitTrackee:
    """
    FitTrackee class.

    Parameters
    ----------
    timeout : int | float
        Timeout for connection in seconds.
    """

    url = ""
    token = None
    token_header = None
    user = None

    def __init__(self, timeout: int | float = 10000):
        """
        Initialise the class.

        Parameters
        ----------
        timeout : int | float
            Timeout for connection in seconds.
        """
        self.timeout = timeout

    def setUrl(self, url: str) -> None:
        """
        Set url and ensure it is correctly formatted.

        Parameters
        ----------
        url : str
           URL of the server.
        """
        if url.endswith("/"):
            self.url = url
        else:
            self.url = url + "/"

    def setToken(self, token: str) -> None:
        """
        Set the Token.

        Parameters
        ----------
        token : str
            Token for authorizing connection.
        """
        self.token = token
        self.token_header = {"Authorization": f"Bearer {self.token}"}

    def login(self, url: str, email: str, password: str) -> None:
        """
        Login/authenticate with the server.

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
        resp = requests.post(url, json=json, timeout=self.timeout)
        if resp.status_code == 200:
            json = resp.json()
            self.token = json["auth_token"]
            self.setToken(self.token)
            # Get User Info
            return self.getUserInfo()
        return False

    def getUserInfo(self):
        """Get user information."""
        url = self.url + "api/auth/profile"
        resp = requests.get(url, headers=self.token_header, timeout=self.timeout)
        if resp.status_code == 200:
            json = resp.json()
            self.user = json["data"]["username"]
            return True
        return False

    def add_workout(
        self, gpx: str | Path, sport_id: int = 0, equipment_id: str = "", title: str = None, notes: str = ""
    ):
        """
        Add a workout.

        Parameters
        ----------
        gpx : str | Path
            GPX file for workout.
        sport_id : int
            Sport ID.
        equipment_id : str
            Equipment ID.
        title : str
            Title for workout.
        notes : str
            Notes to accompany the workout.
        """
        url = self.url + "api/workouts"
        data = {"sport_id": sport_id, "notes": notes}
        if equipment_id != "":
            data["equipment_ids"] = [equipment_id]
        file = {"file": ("workout.gpx", gpx), "data": (None, str(data).replace("'", '"'))}
        resp = requests.post(url, headers=self.token_header, files=file, timeout=self.timeout)
        if resp.status_code == 201:
            json = resp.json()
            workout_id = json["data"]["workouts"][0]["id"]
            if title is not None and title != "":
                # Rename Workout to set Title
                url = self.url + "api/workouts/" + workout_id
                data = {"title": title}
                resp = requests.patch(url, headers=self.token_header, json=data, timeout=self.timeout)
            return True
        print(resp.json())
        return False

    def add_workout_no_gpx(  # pylint: disable=too-many-arguments
        self,
        date: str,
        duration: int | float,
        distance: float,
        sport_id: int = 0,
        title: str = None,
        notes: str = "",
        ascent: int | float = None,
        descent: int | float = None,
    ):
        """
        Add workout without GPX file.

        Parameters
        ----------
        date : str
            Date.
        duration : int | float
            Duration of work out in minutes.
        distance : float
            Distance travelled.
        sport_id : int
            Sport ID.
        title : str
            Title for workout.
        notes : str
            Notes to accompany workout.
        ascent : int | float
            Gain in altitude.
        descent : int | float
            Loss of altitude.
        """
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
        resp = requests.post(url, headers=self.token_header, json=data, timeout=self.timeout)
        if resp.status_code == 201:
            return True
        print(resp.json())
        return False

    def get_sports(self, only_active: bool = False) -> list | None:
        """
        Get available spots.

        Parameters
        ----------
        only_active : bool
            Only get active sports.
        """
        url = self.url + "api/sports"
        resp = requests.get(url, headers=self.token_header, timeout=self.timeout)
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

    def get_equipment(self, only_active: bool = False) -> list | None:
        """
        Get equipment spots.

        Parameters
        ----------
        only_active : bool
            Only get active equipment.
        """
        url = self.url + "api/equipments"
        resp = requests.get(url, headers=self.token_header, timeout=self.timeout)
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
