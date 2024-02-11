"""List of strings used in the app.

https://support.google.com/waze/partners/answer/13458165?sjid=8175537062065788260-EU#zippy=%2Ctraffic-alerts%2Cdata-elements%2Cjson%2Ctraffic-alerts-examples%2Cjson-format%2Calert-types


"""

alert_types = {
    "ACCIDENT": "Accident",
    "JAM": "Traffic Jam",
    "WEATHERHAZARD": "Weather Hazard",
    "HAZARD": "Hazard",
    "MISC": "Miscellaneous",
    "CONSTRUCTION": "Construction",
    "ROAD_CLOSED": "Road Closed",
}

alert_subtypes = {
    "ACCIDENT_MINOR": "Minor Accident",
    "ACCIDENT_MAJOR": "Major Accident",
    "JAM_MODERATE_TRAFFIC": "Moderate Traffic",
    "JAM_HEAVY_TRAFFIC": "Heavy Traffic",
    "JAM_STAND_STILL_TRAFFIC": "Standstill Traffic",
    "JAM_LIGHT_TRAFFIC": "Light Traffic",
    "HAZARD_ON_ROAD": "Hazard on Road",
    "HAZARD_ON_SHOULDER": "Hazard on Shoulder",
    "HAZARD_WEATHER": "Weather Hazard",
    "HAZARD_ON_ROAD_POT_HOLE": "Pothole",
    "HAZARD_ON_ROAD_OBJECT": "Object on Road",
    "HAZARD_ON_ROAD_ROAD_KILL": "Roadkill",
    "HAZARD_ON_SHOULDER_CAR_STOPPED": "Car Stopped on Shoulder",
    "HAZARD_ON_SHOULDER_ANIMALS": "Animals on Shoulder",
    "HAZARD_ON_SHOULDER_MISSING_SIGN": "Missing Sign on Shoulder",
    "HAZARD_WEATHER_FOG": "Fog",
    "HAZARD_WEATHER_HAIL": "Hail",
    "HAZARD_WEATHER_HEAVY_RAIN": "Heavy Rain",
    "HAZARD_WEATHER_HEAVY_SNOW": "Heavy Snow",
    "HAZARD_WEATHER_FLOOD": "Flood",
    "HAZARD_WEATHER_MONSOON": "Monsoon",
    "HAZARD_WEATHER_TORNADO": "Tornado",
    "HAZARD_WEATHER_HEAT_WAVE": "Heat Wave",
    "HAZARD_WEATHER_HURRICANE": "Hurricane",
    "HAZARD_WEATHER_FREEZING_RAIN": "Freezing Rain",
    "HAZARD_ON_ROAD_LANE_CLOSED": "Lane Closed",
    "HAZARD_ON_ROAD_OIL": "Oil on Road",
    "HAZARD_ON_ROAD_ICE": "Ice on Road",
    "HAZARD_ON_ROAD_CONSTRUCTION": "Construction on Road",
    "HAZARD_ON_ROAD_CAR_STOPPED": "Car Stopped on Road",
    "HAZARD_ON_ROAD_TRAFFIC_LIGHT_FAULT": "Traffic Light Fault",
    "ROAD_CLOSED_HAZARD": "Road Closed due to Hazard",
    "ROAD_CLOSED_CONSTRUCTION": "Road Closed due to Construction",
    "ROAD_CLOSED_EVENT": "Road Closed due to Event",
}
