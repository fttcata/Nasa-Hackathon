import meteomatics.api as api
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# ==============================
# Replace with your demo credentials
USERNAME = "berencei_zsolt"
PASSWORD = "h25C2z01udSOT41OtVRZ"
# ==============================

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

# --- MODIFIED: No specific activity parameters for Meteomatics query ---
# The actual parameters queried will always be t_mean_2m_24h:C and precip_24h:mm.
# The 'activity' selection in the frontend will ONLY influence the Google Places search query.
activity_dict = {
  "Unspecified": [], # No specific Meteomatics params derived from these any more
  "Outdoor Celebration": [],
  "Hiking": [],
  "Fishing": [],
  "Swimming": [],
  "Skiing": [],
  "Camping": [],
  "Outdoor Exercise": [],
  "Wind Sailing": [],
  "Sunny": [],
  "Cloudy": [],
  "Rainy": [],
  "Windy": [],
  "beaches": [],
  "hiking trails": [],
  "ski resorts": [],
  "museum": [], # Example of Google Places query term
  "castle": [],
  "national park": [],
  "Other": []
}

# --- Weather Calculation Functions ---

def calc_avg_weather(input_df):
    """
    Calculates the 10-year average for each weather variable for each specific date.
    Assumes input_df columns are already daily aggregated parameters.

    Args:
        input_df (pd.DataFrame): Input DataFrame with daily weather data
                                 over multiple years. It should have 'year', 'month', 'day' columns.

    Returns:
        pd.DataFrame: A DataFrame with the average over X years data for each
                      date (month-day combination) for each attribute.
    """
    if input_df.empty:
        return pd.DataFrame()

    # We expect only t_mean_2m_24h:C and precip_24h:mm, plus date columns
    avg_cols = ["t_mean_2m_24h:C", "precip_24h:mm"]

    # Convert relevant columns to numeric, coercing errors to NaN
    # Then group by month and day, and calculate the mean
    average_df = round(
        input_df[avg_cols].apply(pd.to_numeric, errors='coerce')
        .groupby([input_df['month'], input_df['day']])
        .mean(),
        1
    )
    
    # Rename the index for clarity (e.g., (3, 1) becomes '03-01')
    average_df.index = average_df.index.map(lambda x: f"{x[0]:02d}-{x[1]:02d}")
    average_df.index.name = 'Month-Day'

    return average_df


def get_weather_data(latitude, longitude, start_month, start_day, end_month, end_day): # Removed activity_type from args
    """
    Fetches historical weather data for a given location and date range over the past X years,
    always querying for average temperature and precipitation.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        start_month (int): Start month for the date range.
        start_day (int): Start day for the date range.
        end_month (int): End month for the date range.
        end_day (int): End day for the date range.

    Returns:
        pd.DataFrame: DataFrame containing the X-year averaged weather data for the specified dates.
    """
    coordinates = [(latitude, longitude)]
    
    current_year = datetime.today().year
    years = range(current_year - 10, current_year) # Get data from 10 years ago up to last year

    all_dfs = []

    # --- MODIFIED: Always query these two specific parameters ---
    selected_parameters_for_query = ["t_mean_2m_24h:C", "precip_24h:mm"]

    interval = timedelta(days=1)

    for year in years:
        try:
            current_startdate = datetime(year, start_month, start_day, 0, 0)
            current_enddate = datetime(year, end_month, end_day, 0, 0)

            if current_enddate < current_startdate:
                current_enddate = datetime(year + 1, end_month, end_day, 0, 0)
            
            try:
                datetime(year, start_month, start_day)
                datetime(year, end_month, end_day)
            except ValueError:
                print(f"Skipping year {year} for {latitude},{longitude} due to invalid date for {start_month}/{start_day} or {end_month}/{end_day}")
                continue

            df = api.query_time_series(
                coordinates,
                current_startdate,
                current_enddate,
                interval,
                selected_parameters_for_query, # Use the fixed two parameters
                username=USERNAME,
                password=PASSWORD,
                model="mix"
            )

            df = df.reset_index()

            df["validdate"] = pd.to_datetime(df["validdate"])
            df["year"] = df["validdate"].dt.year
            df["month"] = df["validdate"].dt.month
            df["day"] = df["validdate"].dt.day
            df.drop(columns="validdate", inplace=True)
            all_dfs.append(df)
        except Exception as e:
            print(f"Error fetching data for year {year} at {latitude},{longitude}: {e}")
            continue

    if not all_dfs:
        return pd.DataFrame()

    final_df = pd.concat(all_dfs, ignore_index=True)
    
    pred_df = calc_avg_weather(final_df)
    
    return pred_df

# --- Flask Routes ---

@app.route("/api/get_weather", methods=["GET"])
def get_weather():
    try:
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))
        start_month = int(request.args.get("start_month"))
        start_day = int(request.args.get("start_day"))
        end_month = int(request.args.get("end_month"))
        end_day = int(request.args.get("end_day"))
        # activity is still received from frontend but not used for Meteomatics query
        activity = request.args.get("activity", "Unspecified") 

        # --- MODIFIED: Removed activity parameter from get_weather_data call ---
        weather_averages_df = get_weather_data(lat, lng, start_month, start_day, end_month, end_day)

        if weather_averages_df.empty:
            return jsonify({"status": "error", "message": "No weather data available for the specified range/location."}), 404

        output_data = []
        for param_name in weather_averages_df.columns:
            param_data = {
                "parameter": param_name,
                "coordinates": [
                    {
                        "lat": lat,
                        "lon": lng,
                        "dates": []
                    }
                ]
            }
            for month_day_str, value in weather_averages_df[param_name].items():
                param_data["coordinates"][0]["dates"].append({
                    "date": f"2000-{month_day_str}T00:00:00Z", 
                    "value": value
                })
            output_data.append(param_data)

        return jsonify({"status": "OK", "data": output_data})

    except ValueError as e:
        return jsonify({"status": "error", "message": f"Invalid parameter: {e}"}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"status": "error", "message": f"An internal server error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
