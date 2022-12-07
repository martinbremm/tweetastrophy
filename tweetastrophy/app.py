import streamlit as st
from preprocessing import preprocessing, tokenize_text
import folium
import streamlit as st
from streamlit_folium import st_folium, folium_static

from location import extract_gps, extract_location
from predict import get_prediction
import numpy as np
import pandas as pd

st.set_page_config(page_title='Tweetastrophy', page_icon=':tada:', layout='wide')


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

st.markdown("""
<style>
.big-font {
    font-size:30px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.mid-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(hide_menu, unsafe_allow_html=True)

local_css("tweetastrophy/config.toml")

@st.cache(suppress_st_warning=True, max_entries=100000,
          hash_funcs={'folium.folium.Map':hash})

def plot_map(text):
    text_archive = []

    # creating location df
    text_archive.append(text)
    text_df = pd.DataFrame.from_dict(data={"text": text_archive})
    df_dict = text_df.to_dict("records")

    # looping over text entries in text archive and extracting locations
    dictionary_list = []
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

    map = folium.Map(location=[df.lat,
                            df.lon],
                    tiles="cartodbpositron",
                    zoom_start=3, control_scale=True)

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

    map.fit_bounds([sw, ne], padding=(1,1), max_zoom=10)
    # render Folium map in Streamlit

    return map
with st.sidebar:
    a, b = st.columns([2, 30])
    with a:
        st.text("")
        st.image("tweetastrophy/Twitter-logo.svg.webp", width=60)
    with b:
        st.title('Tweetastrophy')

    st.text("")
    with st.container() :
        #st.markdown('<p class="mid-font"> Enter your tweet here 👇🏼 !!</p>', unsafe_allow_html=True)
        st.info('Enter your tweet here 👇🏼 !!')
        txt = st.text_area('', placeholder='. . .')
        st.button('Predict')

prediction = get_prediction(txt)

prediction_container = st.container()
col1, col2 = st.columns([8,17])

if prediction == 'The tweet is Disaster Tweet':
    with col1:
        st.markdown('<p class="big-font"> The tweet is Disaster Tweet !!</p>', unsafe_allow_html=True)
    with col2:
        st.image("tweetastrophy/warning.png",
            width=40)
    st_folium(plot_map(txt), width=2000)

elif prediction == 'The tweet is Non Disaster Tweet':
    with col1:
        st.markdown('<p class="big-font"> The tweet is Non Disaster Tweet !!</p>', unsafe_allow_html=True)
    with col2:
        st.image("tweetastrophy/safety-icon.png",
            width=40)
    st_folium(plot_map(txt), width=2000)

else:
    st.markdown('<p class="big-font">Waiting for your tweet.. &#128564; </p>', unsafe_allow_html=True)
    st.stop()
