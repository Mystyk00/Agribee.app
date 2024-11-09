import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError, Timeout
from urllib3.util.retry import Retry

def get_soil_type(lat, lon):
    url = f"https://rest.soilgrids.org/soilgrids/v2.0/properties/query?lat={lat}&lon={lon}&property=taxonomy"
    
    # Set up retry strategy with the correct parameter name
    retry_strategy = Retry(
        total=5,  # Total retries
        backoff_factor=1,  # Wait 1s, then 2s, then 4s, etc.
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
        allowed_methods=["GET"]  # Use "allowed_methods" instead of "method_whitelist"
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    
    try:
        response = http.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes

        data = response.json()
        soil_type = data['properties']['soil taxonomy'][0]['classification'][0]['usda_soil_order']
        return soil_type
    except (ConnectionError, HTTPError, Timeout) as e:
        return f"Error: Could not retrieve soil data due to {e}"

# Example usage:
latitude = 34.05
longitude = -118.25

soil_type = get_soil_type(latitude, longitude)
print(f"Soil type at the location ({latitude}, {longitude}): {soil_type}")
