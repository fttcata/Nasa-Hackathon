from flask import Flask, render_template, request
from weather_api import WeatherAPI
from activities import get_parameters_for_activity
import config
from datetime import datetime

app = Flask(__name__)

# Activies and their required parameters (activities.py)
@app.route('/')
def index():
    activities = [
        "Unspecified", "Outdoor Celebration", "Hiking", "Fishing",
        "Swimming", "Skiing", "Camping", "Outdoor Exercise", "Wind Sailing"
    ]
    return render_template('index.html', activities=activities)

# Handle form submission and display weather data
@app.route('/weather', methods=['POST'])
def weather():
    activity = request.form['activity']
    time_input = request.form['datetime']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])

    try:
        user_datetime = datetime.strptime(time_input, "%Y-%m-%d %H:%M")
    except ValueError:
        return render_template('error.html', message="Invalid time format. Use YYYY-MM-DD HH:MM")

    parameters = get_parameters_for_activity(activity)
    api = WeatherAPI(config.username, config.password, parameters)
    weather_data = api.get_weather_data(latitude, longitude, user_datetime)

    return render_template('result.html', activity=activity, weather=weather_data)