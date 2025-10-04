import requests
import activities
import config
from requests.exceptions import HTTPError, RequestException
from datetime import datetime

class WeatherAPI:
    def __init__(self,username,password,parameters):
        self.username = username
        self.password = password
        self.parameters = parameters
    def get_weather_data(self, latitude, longitude,user_datetime):
    # Coordinates:

        self.latitude = latitude
        self.longitude = longitude
    # Parameters    
        validdatetime = user_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")  # Current date and time in ISO 8601 format
        parameters = "t_2m:C,precip_1h:mm,wind_speed_10m:ms,relative_humidity_2m:p" 
        # ",wind_speed_10m:ms,humidity_2m:p" 
     
        format = "json"


    # Construct the API URL
       
        site_url = f"https://{self.username}:{self.password}@api.meteomatics.com/{validdatetime}/{parameters}/{self.latitude},{self.longitude}/{format}"
        try:
            response = requests.get(site_url)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            weather_data = response.json()  # Parse the JSON response
            return weather_data
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        except ValueError as json_err:
            print(f"JSON decoding error: {json_err}")
        

latitude = 53.3498
longitude = -6.2603
api = WeatherAPI(config.username, config.password, activities.parameters)
weather = api.get_weather_data(latitude, longitude) 
print(weather)
