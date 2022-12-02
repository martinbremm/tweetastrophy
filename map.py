# changing the directory in which file looks for our modules
import sys
import os
from os.path import dirname, abspath, join

cwd = os.getcwd()
code = abspath(join(cwd, 'tweetastrophy'))
sys.path.append(code)

# imports
from get_data import get_data
from preprocessing import preprocessing
from location import creat_location
import pandas as pd

# mapping imports
import folium
import streamlit as st
from streamlit_folium import st_folium



# creating location df
df = creat_location("../tweetastrophy/tweets.text")

# creating basic map in folium
map = folium.Map(location=[df.lat.mean(),
                           df.lon.mean()],
                 tiles="cartodbpositron",
                 zoom_start=50, control_scale=True)


# mapping circles to df in DataFrame
for index, row in df.iterrows():
    # checking for rows without coordinates
    if row["lat"] == 0.0 or row["lon"] == 0.0:
        continue

    elif row["city"] != "Unknown":
        folium.CircleMarker(location=[row["lat"], row["lon"]], radius=10, popup=row["city"],
                            color="#EE4B2B", fill=True, fill_color="#EE4B2B").add_to(map) # red
    elif (row["region"] != "Unknown") & (row["city"] == "Unknown"):

        folium.CircleMarker(location=[row["lat"], row["lon"]], radius=20, popup=row["region"],
                            color="#90ee90", fill=True, fill_color="#90ee90").add_to(map) # green

    elif (row["country"] != "Unknown") & (row["region"] == "Unknown") & (row["city"] == "Unknown"):
        folium.CircleMarker(location=[row["lat"], row["lon"]], radius=30, popup=row["country"],
                            color="#00008b", fill=True, fill_color="#00008b").add_to(map) # blue


# adding automatic zoom to last df
sw = df[['lat', 'lon']].min().values.tolist()
ne = df[['lat', 'lon']].max().values.tolist()

map.fit_bounds([sw, ne], padding=(1,1))

# render Folium map in Streamlit
st_data = st_folium(map)
