from langchain_core.tools import tool

import requests, math



# ============================================================
# TOOL 1: RAIN STATUS CHECK
# ============================================================

@tool
def rain_status_check(location: str) -> str:
    """
    Check today's maximum probability of rain
    for a given location.
    """

    # Geocoding API

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 1
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()


    # Extract location details

    location_data = data["results"][0]

    location_name = location_data["name"]

    latitude = location_data["latitude"]
    longitude = location_data["longitude"]


    # Weather API

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "precipitation_probability_max"
        ],
        "timezone": "auto",
        "forecast_days": 1
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_data = weather_response.json()

    daily_data = weather_data["daily"]

    date = daily_data["time"][0]

    rain_probability = (
        daily_data["precipitation_probability_max"][0]
    )

    return (
        f"Rain probability in {location_name} "
        f"on {date}: {rain_probability}%"
    )


# ============================================================
# TOOL 2: TEMPERATURE CHECK
# ============================================================

@tool
def temperature_check(location: str) -> str:
    """
    Check today's maximum and minimum temperature
    for a given location.
    """

    # Geocoding API

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 1
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()


    # Extract location details

    location_data = data["results"][0]

    location_name = location_data["name"]

    latitude = location_data["latitude"]
    longitude = location_data["longitude"]


    # Weather API

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min"
        ],
        "timezone": "auto",
        "forecast_days": 1
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_data = weather_response.json()

    daily_data = weather_data["daily"]

    date = daily_data["time"][0]

    max_temperature = (
        daily_data["temperature_2m_max"][0]
    )

    min_temperature = (
        daily_data["temperature_2m_min"][0]
    )

    return (
        f"Temperature in {location_name} on {date}: "
        f"Minimum {min_temperature}°C, "
        f"Maximum {max_temperature}°C"
    )

# ============================================================
# TOOL 3: WEATHER CONDITIONS
# ============================================================

@tool
def weather_conditions(location: str) -> str:
    """
    Check the current weather conditions for a location.

    Returns current temperature, humidity,
    wind speed and weather condition.
    """

    # Geocoding API

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 1
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    location_data = data["results"][0]

    location_name = location_data["name"]

    latitude = location_data["latitude"]
    longitude = location_data["longitude"]


    # Weather API

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "weather_code"
        ],
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_data = weather_response.json()

    current = weather_data["current"]

    temperature = current["temperature_2m"]

    humidity = current["relative_humidity_2m"]

    wind_speed = current["wind_speed_10m"]

    weather_code = current["weather_code"]


    # Convert weather code into readable text

    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Heavy drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm"
    }

    condition = weather_codes.get(
        weather_code,
        "Unknown weather condition"
    )

    return (
        f"Current weather in {location_name}: "
        f"Temperature {temperature}°C, "
        f"Humidity {humidity}%, "
        f"Wind speed {wind_speed} km/h, "
        f"Condition: {condition}"
    )


# ============================================================
# TOOL 3: CALCULATOR
# ============================================================

@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.

    Supports basic arithmetic and mathematical functions such as:
    log, log10, sqrt, sin, cos, tan, and other math operations.
    """

    try:

        allowed_functions = {
            "log": math.log,
            "log10": math.log10,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(
            expression,
            {"__builtins__": {}},
            allowed_functions
        )

        return f"Result: {result}"

    except Exception as e:
        return f"Calculation error: {str(e)}"