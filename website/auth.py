from flask import Blueprint, render_template, request, flash
from .copy import soil, get_top_plants_by_conditions_city, get_top_plants_by_prices, get_top_plants_by_conditions_coor
import pandas as pd

auth = Blueprint('auth', __name__)

def is_float(string):
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False
    

@auth.route('/map', methods=['GET'])
def show_map_ajax():
    return render_template("map_ajax.html")

@auth.route('/map_data', methods=['GET'])
def show_map_data():
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    if True:
        location = request.args.get('location');
        api_key = "3870ece1b4577e1fa7ff617d9923e4d7"
        soil_type = soil()


        if not location:
            return render_template("map_data.html", error="Location input cannot be empty.")

        try:
            city_name, country = map(str.strip, location.split(', '))
            
            if is_float(city_name) and is_float(country):
                lat = city_name
                lon = country
                df1 = get_top_plants_by_conditions_coor(lat, lon, soil_type, api_key)
                df2 = get_top_plants_by_prices(soil_type)
            else:
                df1 = get_top_plants_by_conditions_city(city_name, soil_type, api_key)
                df2 = get_top_plants_by_prices(soil_type)

        except ValueError:
            return render_template("map_data.html", error="Please enter a valid location as 'city, country' or 'lat, lon'")
        
    return render_template("map_data.html",
                       tables=[df1.to_html(classes='data', index=False), df2.to_html(classes='data', index=False)],
                       titles=[df1.columns.values, df2.columns.values])
    
# @auth.route('/map', methods=['GET', 'POST'])
# def show_map():
#     df1 = pd.DataFrame()
#     df2 = pd.DataFrame()
#     if request.method == 'POST':
#         location = request.form.get('locationInput')
#         api_key = "3870ece1b4577e1fa7ff617d9923e4d7"
#         soil_type = soil()

#         if not location:
#             flash("City name or locations can't be identified", category='error')
#             return render_template("map.html", boolean=False, error="Location input cannot be empty.")

#         try:
#             city_name, country = map(str.strip, location.split(', '))
            
#             if is_float(city_name) and is_float(country):
#                 lat = city_name
#                 lon = country
#                 df1 = get_top_plants_by_conditions_coor(lat, lon, soil_type, api_key)
#                 df2 = get_top_plants_by_prices(soil_type)
#             else:
#                 df1 = get_top_plants_by_conditions_city(city_name, soil_type, api_key)
#                 df2 = get_top_plants_by_prices(soil_type)

#         except ValueError:
#             return render_template("map.html", boolean=False, error="Please enter location as 'city, country' or 'lat, lon'")


#     return render_template("map.html",
#                        tables=[df1.to_html(classes='data'), df2.to_html(classes='data')],
#                        titles=[df1.columns.values, df2.columns.values],
#                        boolean=True)

