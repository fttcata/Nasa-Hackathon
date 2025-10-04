from flask import Flask, render_template, request, jsonify
from weather_api import WeatherAPI
from activities import get_parameters_for_activity
import config
from datetime import datetime
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

api = WeatherAPI(config.username, config.password, [])  # parameters will come from JS

@app.route('/')
def index():
    return render_template('index.html')

# NEW JSON API endpoint
@app.route('/api/weather', methods=['POST'])
def api_weather():
    data = request.get_json()  # important for fetch
    lat = data.get('lat')
    lng = data.get('lng')
    activities = data.get('activities', ['Unspecified'])
    time_input = data.get('datetime')  # optional: JS can send datetime

    if lat is None or lng is None:
        return jsonify({"error": "Missing latitude or longitude"}), 400

    # Convert string datetime to datetime object if provided
    if time_input:
        try:
            user_datetime = datetime.strptime(time_input, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Invalid datetime format"}), 400
    else:
        from datetime import timezone
        user_datetime = datetime.now(timezone.utc)

    # Collect parameters from all selected activities
    parameters = []
    for activity in activities:
        parameters += get_parameters_for_activity(activity)

    weather_api = WeatherAPI(config.username, config.password, parameters)
    weather_data = weather_api.get_weather_data(lat, lng, user_datetime)

    if not weather_data or "data"  not in weather_data:
        return jsonify({"error": "No weather data available"}), 500

    # Simplify response
    simplified = {d["parameter"]: d["coordinates"][0]["dates"][0]["value"]
                  for d in weather_data["data"]}

    return jsonify(simplified)  # return JSON, not HTML
