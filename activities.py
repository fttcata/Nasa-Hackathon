activity_map = {
    "Unspecified": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms", "relative_humidity_2m:p"
    ],
    "Outdoor Celebration": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms"
    ],
    "Hiking": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms",
        "relative_humidity_2m:p", "forest_fire_risk_index", "sunset"
    ],
    "Fishing": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms",
        "cloud_cover:p", "ocean_current_speed:m/s", "ocean_current_direction:d"
    ],
    "Swimming": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms", "relative_humidity_2m:p",
        "uv_index", "ocean_current_speed:m/s", "water_temperature_0m:C", "wave_height:m"
    ],
    "Skiing": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms", "relative_humidity_2m:p",
        "snow_height_0cm:cm", "snowfall_24h:cm", "fresh_snow_24h:cm",
        "cloud_cover:p", "sunrise", "sunset"
    ],
    "Camping": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms", "relative_humidity_2m:p",
        "cloud_cover:p", "sunrise", "sunset"
    ],
    "Outdoor Exercise": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms", "relative_humidity_2m:p", "uv_index"
    ],
    "Wind Sailing": [
        "t_2m:C", "precip_1h:mm", "wind_speed_10m:ms", "relative_humidity_2m:p",
        "cloud_cover:p", "ocean_current_speed:m/s", "ocean_current_direction:d", "wave_height:m"
    ]
}


def get_parameters_for_activity(activity: str):
    return activity_map.get(activity, activity_map["Unspecified"])
