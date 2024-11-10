import requests
import polars as pl
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

        forecast_df = pl.DataFrame(forecast_data, schema=['Temperature', 'Weather Description'])
        
        precipitation_rates = {
            "light rain": 2.5,
            "moderate rain": 7.0,
            "broken clouds": 0.0,
            "overcast clouds": 0.0,
            "clear sky": 0.0,
            "few clouds": 0.0,
            "scattered clouds": 0.0
        }
        
        forecast_df = forecast_df.with_columns(
            (pl.col("Weather Description").map_dict(precipitation_rates) * 365).alias("Precipitation")
        )
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
        
        forecast_df = pl.DataFrame(forecast_data, schema=['Temperature', 'Weather Description'])
        precipitation_rates = {
            "light rain": 2.5,
            "moderate rain": 7.0,
            "broken clouds": 0.0,
            "overcast clouds": 0.0,
            "clear sky": 0.0,
            "few clouds": 0.0,
            "scattered clouds": 0.0
        }
        
        forecast_df = forecast_df.with_columns(
            (pl.col("Weather Description").map_dict(precipitation_rates) * 365).alias("Precipitation")
        )
        
        average_temperature = forecast_df["Temperature"].mean()
        average_precipitation = forecast_df["Precipitation"].mean()
        
        print(average_temperature, average_precipitation)
        return average_temperature, average_precipitation
    else:
        return None, None
def range_to_average(df, column_name):
    # Apply the transformation using Polars expressions
    df = df.with_columns(
        pl.when(pl.col(column_name).str.contains("-"))
        .then(
            pl.col(column_name)
            .str.split("-")
            .arr.eval((pl.element().cast(pl.Float64)), parallel=True)
            .arr.mean()
        )
        .otherwise(pl.col(column_name).cast(pl.Float64))
        .alias(column_name)
    )
    return df
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

price_df = pl.DataFrame(price_data)

# Soil Data
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

# Desired column order
columns_order = ["Plant", "Soil Type", "Temperature", "Humidity", "Precipitation", "Irrigation", "Nitrogen", "Phosphorus", "Potassium"]

# Compiling all soil data into a single dictionary
soil_data_dict = {
    'Chernozem': chernozem_data,
    'Loamy': loamy_data,
    'Sandy': sandy_data,
    'Chestnut': chestnut_data
}

# Create Polars DataFrames for each soil type and convert ranges to averages
soil_dfs = []
for soil_type, soil_data in soil_data_dict.items():
    df = pl.DataFrame(soil_data)
    for col in ["Temperature", "Humidity", "Precipitation", "Irrigation", "Nitrogen", "Phosphorus", "Potassium"]:
        df = df.with_columns(pl.col(col).apply(range_to_average).alias(col))
    soil_dfs.append(df)

# Concatenate all data into a single DataFrame and reorder columns
full_data = pl.concat(soil_dfs).select(columns_order)


def get_top_plants_by_conditions_city(city_name, soil_type, api_key):
    average_temperature, average_precipitation = weather_city(city_name, api_key)
    if average_temperature is None or average_precipitation is None:
        return "City not found or API error."

    filtered_df = full_data.filter(pl.col("Soil Type") == soil_type)
    filtered_df = filtered_df.with_columns([
        abs(pl.col("Temperature") - average_temperature).alias("Temperature Difference"),
        abs(pl.col("Precipitation") - average_precipitation).alias("Precipitation Difference")
    ])
    
    top_3_plants = filtered_df.sort(["Temperature Difference", "Precipitation Difference"]).head(3)
    return top_3_plants.select(columns_order)

def get_top_plants_by_conditions_coor(lat, lon, soil_type, api_key):
    average_temperature, average_precipitation = weather_coor(lat, lon, api_key)
    if average_temperature is None or average_precipitation is None:
        return "City not found or API error."

    filtered_df = full_data.filter(pl.col("Soil Type") == soil_type)
    filtered_df = filtered_df.with_columns([
        abs(pl.col("Temperature") - average_temperature).alias("Temperature Difference"),
        abs(pl.col("Precipitation") - average_precipitation).alias("Precipitation Difference")
    ])
    
    top_3_plants = filtered_df.sort(["Temperature Difference", "Precipitation Difference"]).head(3)
    return top_3_plants.select(columns_order)

def get_top_plants_by_prices(soil_type):
    filtered_df = full_data.filter(pl.col("Soil Type") == soil_type)
    merged_data = filtered_df.join(price_df, left_on="Plant", right_on="Crop", how="inner")
    top_3_plants = merged_data.sort(by=["Soil Type", "Price (UAH/t)"], reverse=[False, True]).head(3)
    return top_3_plants.select(columns_order + ["Price (UAH/t)"])
