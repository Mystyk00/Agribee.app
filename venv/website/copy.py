import requests
import pandas as pd
import random


api_key = "3870ece1b4577e1fa7ff617d9923e4d7"
# Helper Functions
def get_coordinates(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            lat = data[0].get('lat')
            lon = data[0].get('lon')
            return lat, lon
        else:
            return None, None
    else:
        return None, None

def get_city_name(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data.get('name')
        country = data.get('sys', {}).get('country')
        
        if city and country:
            return city, country
        else:
            return "City not found"
    else:
        return f"Error: {response.status_code}"
    
def weather_city(city_name, api_key):
    lat, lon = get_coordinates(city_name, api_key)
    if lat is None or lon is None:
        return None, None

    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forecast_data = [
            (forecast.get('main', {}).get('temp'), forecast.get('weather', [{}])[0].get('description'))
            for forecast in data.get('list', [])
        ]
        
        # Calculate average temperature and precipitation
        forecast_df = pd.DataFrame(forecast_data, columns=['Temperature', 'Weather Description'])
        precipitation_rates = {
            "light rain": 2.5,
            "moderate rain": 7.0,
            "broken clouds": 0.0,
            "overcast clouds": 0.0,
            "clear sky": 0.0,
            "few clouds": 0.0,
            "scattered clouds": 0.0
        }
        forecast_df["Precipitation"] = forecast_df["Weather Description"].map(precipitation_rates) * 365
        average_temperature = forecast_df["Temperature"].mean()
        average_precipitation = forecast_df["Precipitation"].mean()
        print(average_temperature, average_precipitation)
        return average_temperature, average_precipitation
    else:
        return None, None

def weather_coor(lat, lon, api_key):
    if lat is None or lon is None:
        return None, None

    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forecast_data = [
            (forecast.get('main', {}).get('temp'), forecast.get('weather', [{}])[0].get('description'))
            for forecast in data.get('list', [])
        ]
        
        # Calculate average temperature and precipitation
        forecast_df = pd.DataFrame(forecast_data, columns=['Temperature', 'Weather Description'])
        precipitation_rates = {
            "light rain": 2.5,
            "moderate rain": 7.0,
            "broken clouds": 0.0,
            "overcast clouds": 0.0,
            "clear sky": 0.0,
            "few clouds": 0.0,
            "scattered clouds": 0.0
        }
        forecast_df["Precipitation"] = forecast_df["Weather Description"].map(precipitation_rates) * 365
        average_temperature = forecast_df["Temperature"].mean()
        average_precipitation = forecast_df["Precipitation"].mean()
        print(average_temperature, average_precipitation)
        return average_temperature, average_precipitation
    else:
        return None, None


def range_to_average(value):
    if isinstance(value, str) and '-' in value:
        a, b = map(float, value.split('-'))
        return (a + b) / 2
    return float(value)


# Data Definitions
price_data = {
    'Crop': ['Wheat', 'Rye', 'Corn', 'Barley', 'Sunflower', 'Soybean', 'Rapeseed', 'Oats', 'Millet', 'Apple Tree',
             'Pear', 'Grapes', 'Potatoes', 'Cucumbers', 'Tomatoes', 'Cabbage', 'Carrot', 'Beet',
             'Sugar Beet', 'Flax', 'Mustard', 'Peas', 'Lentils', 'Beans',
             'Cherry Tree', 'Plum Tree', 'Apricot Tree', 'Peach Tree', 'Chestnut Tree', 'Fig Tree', 
             'Almond Tree', 'Walnut Tree', 'Hazelnut Tree'],
    'Price (UAH/t)': [
        6500, 4900, 7800, 6500, 17000, 17690, 16936, 4500, 6700, 12000, 12500, 15000, 6000, 8000, 7000, 5000, 4800, 4500, 6000, 7000,  
        8500, 6200, 7500, 8000, 10000, 12000, 11000, 9500, 8000, 8500, 13000, 14000, 11000]
}

price_df = pd.DataFrame(price_data)

# Soil Data
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

# Convert soil data to DataFrames
soil_dfs = []
for data in [chernozem_data, loamy_data, sandy_data, chestnut_data]:
    df = pd.DataFrame(data)
    for col in ["Temperature", "Humidity", "Precipitation", "Irrigation", "Nitrogen", "Phosphorus", "Potassium"]:
        df[col] = df[col].apply(range_to_average)
    soil_dfs.append(df)
full_data = pd.concat(soil_dfs)


# Define the desired column order
columns_order = ["Plant", "Soil Type", "Temperature", "Humidity", "Precipitation", "Irrigation", "Nitrogen", "Phosphorus", "Potassium"]

def get_top_plants_by_conditions_city(city_name, soil_type, api_key):
    average_temperature, average_precipitation = weather_city(city_name, api_key)
    if average_temperature is None or average_precipitation is None:
        return "City not found or API error."

    filtered_df = full_data[full_data["Soil Type"] == soil_type]
    filtered_df.loc[:, "Temperature"] = pd.to_numeric(filtered_df["Temperature"], errors="coerce")
    filtered_df.loc[:, "Precipitation"] = pd.to_numeric(filtered_df["Precipitation"], errors="coerce")
    filtered_df["Temperature Difference"] = abs(filtered_df["Temperature"] - average_temperature)
    filtered_df["Precipitation Difference"] = abs(filtered_df["Precipitation"] - average_precipitation)
    top_3_plants = filtered_df.sort_values(by=["Temperature Difference", "Precipitation Difference"]).head(3)

    # Ensure the output has consistent columns
    return top_3_plants[columns_order].reset_index(drop=True)


def get_top_plants_by_conditions_coor(lat, lon, soil_type, api_key):
    average_temperature, average_precipitation = weather_coor(lat, lon, api_key)
    if average_temperature is None or average_precipitation is None:
        return "City not found or API error."

    filtered_df = full_data[full_data["Soil Type"] == soil_type]
    filtered_df.loc[:, "Temperature"] = pd.to_numeric(filtered_df["Temperature"], errors="coerce")
    filtered_df.loc[:, "Precipitation"] = pd.to_numeric(filtered_df["Precipitation"], errors="coerce")
    filtered_df["Temperature Difference"] = abs(filtered_df["Temperature"] - average_temperature)
    filtered_df["Precipitation Difference"] = abs(filtered_df["Precipitation"] - average_precipitation)
    top_3_plants = filtered_df.sort_values(by=["Temperature Difference", "Precipitation Difference"]).head(3)

    # Ensure the output has consistent columns
    return top_3_plants[columns_order].reset_index(drop=True)


def get_top_plants_by_prices(soil_type):
    filtered_df = full_data[full_data["Soil Type"] == soil_type]
    merged_data = filtered_df.merge(price_df, left_on="Plant", right_on="Crop", how="inner")
    sorted_plants = merged_data.sort_values(by=["Soil Type", "Price (UAH/t)"], ascending=[True, False])
    top_3_plants = sorted_plants.head(3)

    # Ensure the output has consistent columns, including "Price (UAH/t)" if needed
    return top_3_plants[columns_order + ["Price (UAH/t)"]].reset_index(drop=True)
