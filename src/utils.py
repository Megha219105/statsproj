import pandas as pd 
import numpy as np 
import os
import shapely
import pydeck



MAPS = {"e": "Educational", "w": "Work"}
#Colors, increase transparency
GREEN_RGB = [0, 255, 0, 60]
RED_RGB = [240, 100, 0, 60]

#Get data for a specific requirement 

def getMap(df, commute_means, region):
    #Get vars for mapping
    df_selected = df.getregiondata(region)
    homelng, homelat = df.getHomeLoc(region)
    home_col = "SA2_name_h"
    dest_col = "SA2_name_d"
    text = "Number of commutes {"+ commute_means + "} <br /> Commute is from {"+ home_col +"} in red to {"+ dest_col + "} location in green"

    #get Layer first
    arc_layer = pydeck.Layer(
    "ArcLayer",
    data=df_selected,
    get_width=df.getwidthfeature(commute_means),
    get_source_position=df.home_col,
    get_target_position=df.dest_col,
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
    )

    #Create view
    view_state = pydeck.ViewState(
        latitude=homelat, 
        longitude=homelng, 
        bearing=45, 
        pitch=45, 
        zoom=12,)

    #Create pydeck (Now)
    r = pydeck.Deck(
        map_style='mapbox://styles/mapbox/light-v9', 
        layers = [arc_layer], 
        initial_view_state=view_state, 
        tooltip={"html": text})

    return r 

def getxticks(x):
    val = ''
    dict_l = {"Drive_a_car_truck_or_van": "Drive car",
                "Passenger_in_a_car_truck_or_van": "Passenger car",
                "Drive_a_company_car_truck_or_van": "Company vehicle",
                "Drive_a_private_car_truck_or_van": "Private vehicle",
                "Passenger_in_a_car_truck_van_or_company_bus": "Passenger vehicle"}
    if x in list(dict_l.keys()):
        val = dict_l[x]
    else:
        val = x.replace("_", " ")
    return val







