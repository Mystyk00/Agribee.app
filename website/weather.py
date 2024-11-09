import requests
import csv
import pandas as pd
city_name = input("Enter a city name [city,country]: ")
api_key = "3870ece1b4577e1fa7ff617d9923e4d7"

def get_city_name(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data.get('name')
        country = data.get('sys', {}).get('country')
        
        if city and country:
            return f"{city}, {country}"
        else:
            return "City not found"
    else:
        return f"Error: {response.status_code}"
    
def get_coordinates(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if len(data) > 0:
            lat = data[0].get('lat')
            lon = data[0].get('lon')
            print(lat, lon)
            return lat, lon
        else:
            return "City not found", None
    else:
        return f"Error: {response.status_code}", None
    

def weather(city_name, api_key, output_csv="weather_forecast.csv"):
    lat, lon = get_coordinates(city_name, api_key)
    
    if lat is None or lon is None:
        return "City not found or API error."

    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow(['Date & Time', 'Temperature', 'Weather Description'])
            
            forecast_list = data.get('list', [])
            for forecast in forecast_list:
                dt_txt = forecast.get('dt_txt')
                main = forecast.get('main', {})
                temp = main.get('temp')
                weather_desc = forecast.get('weather', [{}])[0].get('description')
                
                writer.writerow([dt_txt, temp, weather_desc])

        print(f"Weather forecast data saved to {output_csv}")
    else:
        return f"Error: {response.status_code}"

weather_t  = weather(city_name, api_key)
print(weather_t)



# number 2
data = {
    'Crop': ['Wheat', 'Rye', 'Corn', 'Barley', 'Sunflower', 'Soybean', 'Rapeseed', 'Oats', 'Millet', 'Apple Tree',
             'Pear', 'Grapes', 'Potatoes', 'Cucumbers', 'Tomatoes', 'Cabbage', 'Carrot', 'Beet',
             'Sugar Beet', 'Flax', 'Mustard', 'Peas', 'Lentils', 'Beans'],
    'Price': [6500, 4900, 7800, 6500, 17000, 17690, 16936, 4500, 6700, 12000, 12500, 15000, 6000, 8000, 7000,
                      5000, 4800, 4500, 6000, 7000, 8500, 6200, 7500, 8000]
}
df = pd.DataFrame(data)
df.to_csv("pricelist.csv", index=False)



# number 3

df = pd.read_csv("weather_forecast.csv")
df["Date & Time"] = pd.to_datetime(df["Date & Time"])
df["Day"] = df["Date & Time"].dt.day

precipitation_rates = {
    "light rain": 2.5,
    "moderate rain": 7.0,
    "broken clouds": 0.0,
    "overcast clouds": 0.0,
    "clear sky": 0.0,
    "few clouds": 0.0,
    "scattered clouds": 0.0
}

df["Precipitation"] = df["Weather Description"].map(precipitation_rates) * 365
df.drop(columns=["Weather Description"], inplace=True)

df.drop(columns=["Date & Time"], inplace=True)
df.to_csv("forecast.csv", index=False)

df = pd.read_csv("forecast.csv")

average_temperature = df["Temperature"].mean()
average_precipitation = df["Precipitation"].mean()

overall_average = pd.DataFrame({
    "Average Temperature": [average_temperature],
    "Average Precipitation": [average_precipitation]
})

overall_average.to_csv("average_data.csv", index=False)
print(overall_average)


def range_to_average(value):
    if isinstance(value, str) and '-' in value:
        a, b = map(float, value.split('-'))
        return (a + b) / 2
    return float(value)

chernozem_data = {
    "Plant": ["Wheat", "Corn", "Sunflower", "Beet", "Barley", "Rapeseed"],
    "Soil Type": ["Chernozem"] * 6,
    "Temperature": ["20", "22", "20", "18", "17", "20"],
    "Humidity": ["60-70", "60-75", "60-70", "65-80", "55-70", "60-75"],
    "Precipitation": ["450-700", "500-800", "450-650", "500-700", "350-550", "500-700"],
    "Irrigation": ["10-20", "15-25", "10-15", "15-20", "5-10", "15-25"],
    "Nitrogen": ["0.06-0.09", "0.07-0.10", "0.08-0.10", "0.06-0.08", "0.04-0.06", "0.07-0.09"],
    "Phosphorus": ["0.04-0.06", "0.03-0.05", "0.03-0.05", "0.04-0.06", "0.02-0.04", "0.03-0.05"],
    "Potassium": ["0.05-0.07", "0.04-0.06", "0.06-0.08", "0.05-0.07", "0.03-0.05", "0.04-0.06"]
}

chernozem_df = pd.DataFrame(chernozem_data)

loamy_data = {
    "Plant": ["Oats", "Peas", "Lentils", "Cabbage", "Cucumbers"],
    "Soil Type": ["Loamy"] * 5,
    "Temperature": ["15", "22", "20", "15", "20"],
    "Humidity": ["60-70", "50-70", "50-70", "70-85", "60-80"],
    "Precipitation": ["350-500", "400-600", "300-500", "450-600", "400-600"],
    "Irrigation": ["5-10", "10-15", "5-10", "15-20", "15-25"],
    "Nitrogen": ["0.06-0.08", "0.04-0.06", "0.04-0.06", "0.05-0.07", "0.06-0.08"],
    "Phosphorus": ["0.02-0.04", "0.03-0.05", "0.02-0.04", "0.04-0.06", "0.03-0.05"],
    "Potassium": ["0.03-0.05", "0.05-0.07", "0.03-0.05", "0.06-0.08", "0.04-0.06"]
}

loamy_df = pd.DataFrame(loamy_data)

sandy_data = {
    "Plant": ["Potatoes", "Tomatoes", "Carrots", "Onions", "Sunflowers"],
    "Soil Type": ["Sandy"] * 5,
    "Temperature": ["15", "24", "17", "20", "20"],
    "Humidity": ["50-60", "60-75", "55-70", "60-70", "60-70"],
    "Precipitation": ["300-500", "450-600", "350-500", "400-600", "450-650"],
    "Irrigation": ["10-15", "15-25", "5-10", "10-15", "10-15"],
    "Nitrogen": ["0.06-0.08", "0.08-0.10", "0.04-0.06", "0.06-0.08", "0.08-0.10"],
    "Phosphorus": ["0.02-0.04", "0.03-0.05", "0.02-0.04", "0.03-0.05", "0.03-0.05"],
    "Potassium": ["0.03-0.05", "0.06-0.08", "0.03-0.05", "0.04-0.06", "0.06-0.08"]
}

sandy_df = pd.DataFrame(sandy_data)

chestnut_data = {
    "Plant": ["Millet", "Barley", "Peas", "Oats", "Wheat"],
    "Soil Type": ["Chestnut"] * 5,
    "Temperature": ["24", "17", "20", "15", "20"],
    "Humidity": ["40-50", "50-70", "50-70", "50-60", "60-70"],
    "Precipitation": ["250-400", "300-500", "400-600", "350-500", "450-700"],
    "Irrigation": ["5-10", "5-10", "10-15", "5-10", "10-20"],
    "Nitrogen": ["0.04-0.06", "0.04-0.06", "0.04-0.06", "0.04-0.06", "0.06-0.09"],
    "Phosphorus": ["0.02-0.04", "0.02-0.04", "0.03-0.05", "0.02-0.04", "0.04-0.06"],
    "Potassium": ["0.03-0.05", "0.03-0.05", "0.05-0.07", "0.03-0.05", "0.05-0.07"]
}

chestnut_df = pd.DataFrame(chestnut_data)

columns_to_convert = ["Temperature", "Humidity", "Precipitation", "Irrigation", "Nitrogen", "Phosphorus", "Potassium"]

for df in [chernozem_df, loamy_df, sandy_df, chestnut_df]:
    for col in columns_to_convert:
        df[col] = df[col].apply(range_to_average)

full_data = pd.concat([chernozem_df, loamy_df, sandy_df, chestnut_df])

full_data.to_csv("combined_soil_data.csv", index=False)

print(full_data)

avg_temp_df = pd.read_csv("average_data.csv")
full_data = pd.read_csv("combined_soil_data.csv")

def filter_plants_by_conditions(soil_type, temperature, precipitation):
    filtered_df = full_data[full_data["Soil Type"] == soil_type]
    
    filtered_df.loc[:, "Temperature"] = pd.to_numeric(filtered_df["Temperature"], errors="coerce")
    filtered_df.loc[:, "Precipitation"] = pd.to_numeric(filtered_df["Precipitation"], errors="coerce")

    filtered_df.loc[:, "Temperature Difference"] = abs(filtered_df["Temperature"] - temperature)
    filtered_df.loc[:, "Precipitation Difference"] = abs(filtered_df["Precipitation"] - precipitation)

    top_3_plants = filtered_df.sort_values(by=["Temperature Difference", "Precipitation Difference"]).head(3)

    top_3_plant_names = top_3_plants["Plant"]
    top_3_full_data = full_data[(full_data["Plant"].isin(top_3_plant_names)) & (full_data["Soil Type"] == soil_type)]
    
    return top_3_full_data

soil_type = "Chernozem"
temperature = avg_temp_df.iloc[0]["Average Temperature"]
precipitation = avg_temp_df.iloc[0]["Average Precipitation"]

top_plants = filter_plants_by_conditions(soil_type, temperature, precipitation)
print(top_plants)

data = {
    'Crop': ['Wheat', 'Rye', 'Corn', 'Barley', 'Sunflower', 'Soybean', 'Rapeseed', 'Oats', 'Millet', 'Apple Tree',
             'Pear', 'Grapes', 'Potatoes', 'Cucumbers', 'Tomatoes', 'Cabbage', 'Carrot', 'Beet',
             'Sugar Beet', 'Flax', 'Mustard', 'Peas', 'Lentils', 'Beans'],
    'Price (UAH/t)': [6500, 4900, 7800, 6500, 17000, 17690, 16936, 4500, 6700, 12000, 12500, 15000, 6000, 8000, 7000,
                      5000, 4800, 4500, 6000, 7000, 8500, 6200, 7500, 8000]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("pricelist.csv", index=False)

avg_temp_df = pd.read_csv("average_data.csv")
full_data = pd.read_csv("combined_soil_data.csv")
price_df = pd.read_csv("pricelist.csv")

def filter_plants_by_prices(soil_type):
    filtered_df = full_data[full_data["Soil Type"] == soil_type]
    
    merged_data = filtered_df.merge(price_df, left_on="Plant", right_on="Crop", how="inner")
    
    sorted_plants = merged_data.sort_values(by=["Soil Type", "Price (UAH/t)"], ascending=[True, False])
    
    top_3_plants = sorted_plants.head(3)
    top_3_plant_names = top_3_plants["Plant"]
    top_3_full_data = full_data[(full_data["Plant"].isin(top_3_plant_names)) & (full_data["Soil Type"] == soil_type)]
    
    return top_3_full_data

soil_type = "Chernozem"

top_plants = filter_plants_by_prices(soil_type)
print(top_plants)
