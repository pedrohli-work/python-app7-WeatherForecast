from datetime import datetime
from typing import List, Tuple
import requests


API_KEY = "Your API KEY"

def get_data(place, forecast_days=None):
    """
    Fetches weather forecast data for a given location using the OpenWeatherMap API.

    Args:
        place (str): The name of the city or location to fetch the forecast for.
        forecast_days (int, optional): The number of days to retrieve. 
                                       Each day contains 8 forecast entries 
                                       (3-hour intervals). Defaults to None.

    Returns:
        list: A list of forecast entries (dictionaries) limited to the requested days. 
              Each entry contains temperature, humidity, weather, and time data.
    """
    # Build the API endpoint URL with the given place and the API key
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    # Send an HTTP GET request to the API
    response = requests.get(url, timeout=10)
    # Convert the API response from JSON format into a Python dictionary
    data = response.json()
    # Extract only the forecast lis
    filtered_data = data["list"]
    # Calculate how many entries to keep based on requested days
    nr_values = 8 * forecast_days
    # Slice the forecast list to keep only the required number of entries
    filtered_data = filtered_data[:nr_values]
    # Return the filtered forecast data
    return filtered_data


def get_lat_lon(place: str) -> Tuple[float, float]:
    """
    Look up latitude and longitude for a given place name using OpenWeather's
    Direct Geocoding API.

    Args:
        place (str): City name (you can include country/region, e.g., "Paris, FR").

    Returns:
        Tuple[float, float]: A pair (lat, lon) for the first matching result.

    Raises:
        ValueError: If no matching city is found.
        Exception: Propagates any unexpected errors (e.g., network issues).
    """
    try:
        # Build the API URL using the place name, limiting results to 1
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={place}&limit=1&appid={API_KEY}"
        # Send a GET request to the OpenWeather Geocoding API
        geo_data = requests.get(geo_url, timeout=10).json()

        # Check if any results were returned
        if not geo_data:
            # Raise error if the city does not exist
            raise ValueError("City not found")
        # Extract latitude and longitude from the first result
        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
        # Return the latitude and longitude as a tuple
        return lat, lon
    
    except Exception as e:
        # Print the error and propagate it
        print(f"Error fetching coordinates: {e}")
        raise


def get_uv_open_meteo(place: str):
    """
    Fetch upcoming UV index values for a given city using Open-Meteo's free API.

    Args:
        place (str): City name (e.g., "Braga, PT").

    Returns:
        List[Tuple[str, float]]: A list of tuples containing the next 6 hours' times
        (formatted as HH:MM) and their corresponding UV index values.
        Returns None if there is an error or no data.

    Notes:
        - Only future hourly values are returned.
        - Limited to the next 6 available hours for simplicity.
        - Does not require an API key.
    """
    try:
         # Get latitude and longitude for the city
        lat, lon = get_lat_lon(place)
        # Construct Open-Meteo API URL for hourly UV index
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=uv_index"
        
        # Send HTTP GET request
        response = requests.get(url, timeout=10)
        # Return None if response status is not 200 OK
        if response.status_code != 200:
            return None
        
        # Parse JSON response
        data = response.json()

        # Extract times and UV index values from the response
        times = data["hourly"]["time"]
        uv_values = data["hourly"]["uv_index"]
        
        # Collect upcoming UV values for future hours
        upcoming_uv = []        
        for t, uv in zip(times, uv_values):
            # Convert ISO time string to datetime object
            dt = datetime.fromisoformat(t)
            # Only keep future times
            if dt > datetime.now():
                # Format as HH:MM
                upcoming_uv.append((dt.strftime("%H:%M"), uv))
            # Limit to next 6 hours
            if len(upcoming_uv) >= 6:
                break
        # Return the list of upcoming UV tuples
        return upcoming_uv
    
    except Exception as e:
        # Print the error and return None if anything goes wrong
        print(f"Error fetching UV from Open-Meteo: {e}")
        return None


def get_aqi(place: str) -> List[int]:
    """
    Fetch Air Quality Index (AQI) values for a given city using OpenWeather's Air Pollution API.

    Args:
        place (str): City name (you can include country/region, e.g., "Paris, FR").

    Returns:
        List[int]: A list of AQI values for the upcoming forecast hours.
                   Returns an empty list if an error occurs.

    Notes:
        - AQI values are typically integers: 1 (Good) to 5 (Hazardous).
        - Requires a valid OpenWeather API key (API_KEY).
    """
    try:
        # Get latitude and longitude for the city
        lat, lon = get_lat_lon(place)
        # Construct the API URL for AQI forecast
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
        # Send an HTTP GET request and parse the JSON response
        aqi_data = requests.get(aqi_url, timeout=10).json()
        
        # 4. Extract AQI values from the JSON data
        #    - Iterate over each item in 'list'
        #    - Use item["main"].get("aqi", 0) to get AQI or 0 if missing
        aqi_values = [item["main"].get("aqi", 0) for item in aqi_data.get("list", [])]
        # 5. Return the list of AQI values
        return aqi_values
    
    except Exception as e:
        # Print any error and return empty list in case of failure
        print(f"Error fetching AQI: {e}")
        return []

if __name__ == "__main__":
    # Quick tests
    city = "Tokyo"

    print("=== Forecast ===")
    forecast = get_data(place=city, forecast_days=3)
    print(forecast)

    print("\n=== Latitude e Longitude ===")
    try:
        lat, lon = get_lat_lon(city)
        print(f"{city}: lat={lat}, lon={lon}")
    except Exception as e:
        print(f"Error fetching lat/lon: {e}")

    print("\n=== UV (Open-Meteo) ===")
    uv_data = get_uv_open_meteo(city)
    if uv_data:
        for t, uv in uv_data:
            print(f"{t} - UV: {uv}")
    else:
        print("No UV data available")

    print("\n=== Air Quality Index ===")
    aqi = get_aqi(place=city)
    print(aqi)
