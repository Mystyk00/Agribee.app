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




chernozem_data = {
    "Plant": ["Wheat", "Corn", "Sunflower", "Beet", "Barley", "Rapeseed", "Cherry Tree", "Plum Tree", "Apricot Tree"],
    "Soil Type": ["Chernozem"] * 9,
    "Temperature": ["20", "22", "20", "18", "17", "20", "22", "20", "20"],
    "Humidity": ["60-70", "60-75", "60-70", "65-80", "55-70", "60-75", "60-70", "50-70", "50-70"],
    "Precipitation": ["450-700", "500-800", "450-650", "500-700", "350-550", "500-700", "500-600", "500-600", "500-600"],
    "Irrigation": ["10-20", "15-25", "10-15", "15-20", "5-10", "15-25", "15-20", "10-15", "10-15"],
    "Nitrogen": ["0.06-0.09", "0.07-0.10", "0.08-0.10", "0.06-0.08", "0.04-0.06", "0.07-0.09", "0.08-0.10", "0.06-0.09", "0.06-0.09"],
    "Phosphorus": ["0.04-0.06", "0.03-0.05", "0.03-0.05", "0.04-0.06", "0.02-0.04", "0.03-0.05", "0.03-0.05", "0.03-0.05", "0.03-0.05"],
    "Potassium": ["0.05-0.07", "0.04-0.06", "0.06-0.08", "0.05-0.07", "0.03-0.05", "0.04-0.06", "0.06-0.08", "0.05-0.07", "0.05-0.07"]
}

loamy_data = {
    "Plant": ["Oats", "Peas", "Lentils", "Cabbage", "Cucumbers", "Apple Tree", "Peach Tree", "Pear Tree"],
    "Soil Type": ["Loamy"] * 8,
    "Temperature": ["15", "22", "20", "15", "20", "20", "22", "20"],
    "Humidity": ["60-70", "50-70", "50-70", "70-85", "60-80", "60-70", "50-70", "60-70"],
    "Precipitation": ["350-500", "400-600", "300-500", "450-600", "400-600", "500-600", "450-600", "500-600"],
    "Irrigation": ["5-10", "10-15", "5-10", "15-20", "15-25", "10-15", "15-20", "10-15"],
    "Nitrogen": ["0.06-0.08", "0.04-0.06", "0.04-0.06", "0.05-0.07", "0.06-0.08", "0.06-0.08", "0.06-0.08", "0.06-0.08"],
    "Phosphorus": ["0.02-0.04", "0.03-0.05", "0.02-0.04", "0.04-0.06", "0.03-0.05", "0.03-0.05", "0.03-0.05", "0.03-0.05"],
    "Potassium": ["0.03-0.05", "0.05-0.07", "0.03-0.05", "0.06-0.08", "0.04-0.06", "0.04-0.06", "0.04-0.06", "0.04-0.06"]
}

sandy_data = {
    "Plant": ["Potatoes", "Tomatoes", "Carrots", "Onions", "Sunflowers", "Cherry Tree", "Fig Tree", "Almond Tree"],
    "Soil Type": ["Sandy"] * 8,
    "Temperature": ["15", "24", "17", "20", "20", "22", "24", "20"],
    "Humidity": ["50-60", "60-75", "55-70", "60-70", "60-70", "60-70", "50-60", "60-70"],
    "Precipitation": ["300-500", "450-600", "350-500", "400-600", "450-650", "400-500", "300-400", "300-500"],
    "Irrigation": ["10-15", "15-25", "5-10", "10-15", "10-15", "10-15", "10-15", "10-15"],
    "Nitrogen": ["0.06-0.08", "0.08-0.10", "0.04-0.06", "0.06-0.08", "0.08-0.10", "0.08-0.10", "0.06-0.08", "0.06-0.08"],
    "Phosphorus": ["0.02-0.04", "0.03-0.05", "0.02-0.04", "0.03-0.05", "0.03-0.05", "0.03-0.05", "0.02-0.04", "0.02-0.04"],
    "Potassium": ["0.03-0.05", "0.06-0.08", "0.03-0.05", "0.04-0.06", "0.06-0.08", "0.06-0.08", "0.03-0.05", "0.03-0.05"]
}

chestnut_data = {
    "Plant": ["Millet", "Barley", "Peas", "Oats", "Wheat", "Chestnut Tree", "Walnut Tree", "Hazelnut Tree"],
    "Soil Type": ["Chestnut"] * 8,
    "Temperature": ["24", "17", "20", "15", "20", "20", "22", "22"],
    "Humidity": ["40-50", "50-70", "50-70", "50-60", "60-70", "60-70", "50-70", "50-70"],
    "Precipitation": ["250-400", "300-500", "400-600", "350-500", "450-700", "300-400", "400-600", "300-400"],
    "Irrigation": ["5-10", "5-10", "10-15", "5-10", "10-20", "5-10", "5-10", "5-10"],
    "Nitrogen": ["0.04-0.06", "0.04-0.06", "0.04-0.06", "0.04-0.06", "0.06-0.09", "0.06-0.09", "0.04-0.06", "0.04-0.06"],
    "Phosphorus": ["0.02-0.04", "0.02-0.04", "0.03-0.05", "0.02-0.04", "0.04-0.06", "0.03-0.05", "0.03-0.05", "0.03-0.05"],
    "Potassium": ["0.03-0.05", "0.03-0.05", "0.05-0.07", "0.03-0.05", "0.05-0.07", "0.04-0.06", "0.03-0.05", "0.03-0.05"]
}

arr = ["Chernozem", "Loamy", "Sandy", "Chestnut"]
def soil():
    soil = arr[random.randint(0,3)]
    return soil