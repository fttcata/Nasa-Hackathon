import requests
from requests.exceptions import HTTPError, RequestException
from datetime import datetime

USERNAME = "petre_andreicatalin"
PASSWORD = "f1vgoYBvtLq48j4P8xW0"

class WeatherAPI:
    def __init__(self, username, password, parameters):
        self.username = username
        self.password = password
        self.parameters = parameters

    def get_weather_data(self, latitude, longitude, user_datetime):
        """Fetch weather data from Meteomatics API."""
        validdatetime = user_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        parameters = ",".join(self.parameters)

        url = f"https://api.meteomatics.com/{validdatetime}/{parameters}/{latitude},{longitude}/json"

        try:
            response = requests.get(url, auth=(self.username, self.password))
            response.raise_for_status()
            return response.json()
        except ValueError as json_err:  #
            print(f"JSON decoding error: {json_err}")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except Exception as err:
            print(f"An unexpected error occurred: {err}")

        return None
    
#test
weather = WeatherAPI("petre_andreicatalin", "f1vgoYBvtLq48j4P8xW0", ["t_2m:C"])
print(weather.get_weather_data(46.770439, 23.591423, datetime(2024, 6, 20, 15, 0)))
