from flask import Flask, render_template_string, request
import requests
from datetime import datetime
from requests.exceptions import HTTPError, RequestException

app = Flask(__name__)

# Meteomatics credentials
USERNAME = "petre_andreicatalin"
PASSWORD = "f1vgoYBvtLq48j4P8xW0"

# Activity mapping for weather parameters
activity_map = {
    "Unspecified": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms,relative_humidity_2m:p"],
    "Outdoor Celebration": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms"],
    "Hiking": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms,relative_humidity_2m:p,forest_fire_risk_index,sunset"],
    "Fishing": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms,cloud_cover:p,ocean_current_speed:m/s,ocean_current_direction:d"],
    "Swimming": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms,relative_humidity_2m:p,uv_index,ocean_current_speed:m/s,water_temperature_0m:C,wave_height:m"],
    "Skiing": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms,relative_humidity_2m:p,snow_height_0cm:cm,snowfall_24h:cm,fresh_snow_24h:cm,cloud_cover:p,sunrise,sunset"],
    "Camping": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms,relative_humidity_2m:p,cloud_cover:p,sunrise,sunset"],
    "Outdoor Exercise": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms,relative_humidity_2m:p,uv_index"],
    "Wind Sailing": ["t_2m:C,precip_1h:mm,wind_speed_10m:ms,relative_humidity_2m:p,cloud_cover:p,ocean_current_speed:m/s,ocean_current_direction:d,wave_height:m"]
}

def get_parameters_for_activity(activity):
    return activity_map.get(activity, activity_map["Unspecified"])

# Meteomatics API wrapper
class WeatherAPI:
    def __init__(self, username, password, parameters):
        self.username = username
        self.password = password
        self.parameters = parameters

    def get_weather_data(self, latitude, longitude, user_datetime):
        validdatetime = user_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        parameters = ",".join(self.parameters)
        url = f"https://{self.username}:{self.password}@api.meteomatics.com/{validdatetime}/{parameters}/{latitude},{longitude}/json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException, ValueError) as e:
            return {"error": str(e)}

# Main page
@app.route('/')
def index():
    activities = list(activity_map.keys())
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WeatherWary.Earth</title>
<style>
body {margin:0;font-family:Arial,sans-serif;display:flex;height:100vh;background:#0f1724;color:#e6eef6;}
#sidebar {width:320px;background:#0b1220;padding:20px;box-sizing:border-box;overflow-y:auto;border-right:1px solid rgba(255,255,255,0.05);text-align:center;}
#logo {width:200px;margin-bottom:12px;}
input,select,button {width:100%;padding:8px;margin-top:6px;border-radius:6px;border:none;background:rgba(255,255,255,0.1);color:#e6eef6;}
button {background:linear-gradient(90deg,#46b3ff,#2bd0a6);color:#022;font-weight:bold;cursor:pointer;}
#map {flex-grow:1;}
label {text-align:left;display:block;margin-top:10px;color:#9aa6b2;font-size:14px;}
</style>
</head>
<body>
<div id="sidebar">
  <img id="logo" src="WheatherWay.1st.png" alt="WeatherWary.Earth Logo">
  <form action="/weather" method="POST">
    <label>Latitude</label>
    <input id="lat" name="latitude" required placeholder="Click on the map or enter lat">

    <label>Longitude</label>
    <input id="lon" name="longitude" required placeholder="Click on the map or enter lon">

    <label>Date & Time</label>
    <input type="datetime-local" name="datetime" required>

    <label>Activity</label>
    <select name="activity">
      {% for act in activities %}
      <option value="{{ act }}">{{ act }}</option>
      {% endfor %}
    </select>

    <button type="submit">Get Weather</button>
  </form>
</div>
<div id="map"></div>
<script>
function initMap(){
  const map=new google.maps.Map(document.getElementById('map'),{center:{lat:20,lng:0},zoom:2});
  map.addListener('click',e=>{
    document.getElementById('lat').value=e.latLng.lat();
    document.getElementById('lon').value=e.latLng.lng();
  });
}
</script>
<script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_API_KEY&callback=initMap"></script>
</body></html>
""", activities=activities)

# Weather data page
@app.route('/weather', methods=['POST'])
def weather():
    try:
        activity = request.form['activity']
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        time_input = request.form['datetime']
        user_datetime = datetime.strptime(time_input, "%Y-%m-%dT%H:%M")
        parameters = get_parameters_for_activity(activity)
        api = WeatherAPI(USERNAME, PASSWORD, parameters)
        weather_data = api.get_weather_data(latitude, longitude, user_datetime)
        return render_template_string("""
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Weather Results</title></head>
<body style="background:#0f1724;color:#e6eef6;font-family:Arial;padding:20px;">
  <h2>Weather for {{ activity }}</h2>
  <pre style="background:#111;padding:10px;border-radius:8px;color:#bdf;">{{ weather | tojson(indent=2) }}</pre>
  <a href="/" style="color:#46b3ff;">← Back</a>
</body></html>
""", activity=activity, weather=weather_data)
    except Exception as e:
        return f"<h3 style='color:red;'>Error: {e}</h3>"

if __name__ == "__main__":
    app.run(debug=True)
