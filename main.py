from flask import Flask, render_template, request
from weather_api import WeatherAPI
from activities import get_parameters_for_activity
import config
from datetime import datetime
import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

print("Current working directory:", os.getcwd())
print("templates folder exists:", os.path.exists("templates"))
print("index.html exists:", os.path.exists("templates/index.html"))
print("result.html exists:", os.path.exists("templates/result.html"))
print("error.html exists:", os.path.exists("templates/error.html"))
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    activity = request.form.get('activity')
    time_input = request.form.get('datetime')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    if not latitude or not longitude:
        return render_template('error.html', message="Please click on the map to select a location.")

    try:
        user_datetime = datetime.strptime(time_input, "%Y-%m-%d %H:%M")
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return render_template('error.html', message="Invalid input. Check time format and coordinates.")

    parameters = get_parameters_for_activity(activity)
    api = WeatherAPI(config.username, config.password, parameters)
    weather_data = api.get_weather_data(latitude, longitude, user_datetime)

    if weather_data and "data" in weather_data:
        simplified = {d["parameter"]: d["coordinates"][0]["dates"][0]["value"]
                  for d in weather_data["data"]}
    else:
        simplified = {}
        if not simplified:
            return render_template('error.html', message="No weather data available for the selected time and location.")
    return render_template('result.html', activity=activity, weather=simplified)

