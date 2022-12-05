import streamlit as st
from get_data import get_data
from preprocessing import preprocessing, tokenize_text
import folium
import streamlit as st
from streamlit_folium import st_folium

from location import extract_gps, extract_location
from model import get_model, get_prediction
import numpy as np
import pandas as pd

text_archive = []

hide_menu = """
<style>
#MainMenu {
    visibility:hidden;

}

footer {
    visibility:hidden;
}
</style>

"""
st.set_page_config(page_title='Tweetastrophy', page_icon=':tada:', layout='centered')

a, b = st.columns([1, 10])

with a:
    st.text("")
    st.image("../tweetastrophy/Twitter-logo.svg.webp", width=50)
with b:
    st.title("Tweetastrophy")



with st.container() :
    txt = st.text_area('Enter your tweet here 👇🏼', '')
    st.button('Predict')
    st.write('', get_prediction(txt))


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(hide_menu, unsafe_allow_html=True)

local_css("config.toml")


# creating location df
text_archive.append(txt)
text_df = pd.DataFrame.from_dict(data={"text": text_archive})
df_dict = text_df.to_dict("records")

# looping over text entries in text archive and extracting locations
dictionary_list = []
coordinates = []
for row in df_dict:
    # creating list of location details
    dic = extract_location(row["text"])
    dic['lat'], dic['lon'] = extract_gps(dic['country'],dic['city'])
    dictionary_list.append(dic)

# putting text and location data into dataframe
locations_df = pd.DataFrame.from_dict(data=dictionary_list)
# only taking first entry
locations_df[['region', 'country', 'city']] = locations_df[['region', 'country', 'city']].applymap(lambda x: x[0])
df = pd.concat([text_df, locations_df], axis=1)

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
        folium.Circle(location=[row["lat"], row["lon"]], radius=10000, popup=row["city"],
                            color="#EE4B2B", fill=True, fill_color="#EE4B2B").add_to(map) # red
    elif (row["region"] != "Unknown") & (row["city"] == "Unknown"):

        folium.Circle(location=[row["lat"], row["lon"]], radius=660000, popup=row["region"],
                            color="#90ee90", fill=True, fill_color="#90ee90").add_to(map) # green

    elif (row["country"] != "Unknown") & (row["region"] == "Unknown") & (row["city"] == "Unknown"):
        folium.Circle(location=[row["lat"], row["lon"]], radius=660000, popup=row["country"],
                            color="#00008b", fill=True, fill_color="#00008b").add_to(map) # blue

# adding automatic zoom to last df
sw = df[['lat', 'lon']].min().values.tolist()
ne = df[['lat', 'lon']].max().values.tolist()

map.fit_bounds([sw, ne], padding=(1,1))

# render Folium map in Streamlit
st_data = st_folium(map)
