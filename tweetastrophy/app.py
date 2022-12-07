import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

from location import create_location
from predict import get_prediction

text_archive = []

# frontend style descriptors
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
st.set_page_config(page_title='Tweetastrophy', page_icon=':tada:', layout='wide')

a, b = st.columns([1, 20])

with a:
    st.text("")
    st.image("tweetastrophy/twitter_logo.png", width=50)
with b:
    st.title("Tweetastrophy")

c, d = st.columns([500, 400])

with c:
    txt = st.text_area('Enter your tweet here 👇🏼', '')
    st.button('Predict')

# creating prediction value
prediction = get_prediction(txt)

with d:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('', prediction)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(hide_menu, unsafe_allow_html=True)

local_css("tweetastrophy/config.toml")




# creating location df
text_archive.append(txt)

text_archive = list(set(text_archive))

if txt == "":
    map = folium.Map(location=[0,0],
                 tiles="cartodbpositron",
                 zoom_start=3, control_scale=True)

    text_archive.remove(txt)

else:

    text_df = pd.DataFrame.from_dict(data={"text": text_archive})

    # looping over text entries in text archive and extracting locations
    locations_df = create_location(text_df)


    # creating basic map in folium
    map = folium.Map(location=[locations_df.lat.mean(), locations_df.lon.mean()],
                    tiles="cartodbpositron",
                    zoom_start=5, min_zoom=3, control_scale=True)

    # mapping circles to df in DataFrame
    df_dict = locations_df.to_dict("records")

    dictionary_list = []

    for row in df_dict:

        if prediction == "The tweet is Disaster Tweet":
            color = "#EE4B2B" # red
        else:
            color = "90ee90" # green

        # checking for rows without coordinates
        if row["lat"] == 0.0 or row["lon"] == 0.0:
            continue

        # city data available
        elif row["city"] != "Unknown":
            if row["size"] == "Not Found":
                radius=10000
            else:
                radius=row["size"]

            folium.Circle(location=[row["lat"], row["lon"]], radius=radius, popup=row["city"],
                                color=color, fill=True, fill_color=color).add_to(map) # red

        # region data available
        elif (row["region"] != "Unknown") & (row["city"] == "Unknown"):
            if row["size"] == "Not Found":
                radius=660000
            else:
                radius=row["size"]

            folium.Circle(location=[row["lat"], row["lon"]], radius=radius, popup=row["region"],
                                color=color, fill=True, fill_color=color).add_to(map) # green

        # country data available
        elif (row["country"] != "Unknown") & (row["region"] == "Unknown") & (row["city"] == "Unknown"):
            if row["size"] == "Not Found":
                radius=660000
            else:
                radius=row["size"]

            folium.Circle(location=[row["lat"], row["lon"]], radius=660000, popup=row["country"],
                                color=color, fill=True, fill_color=color).add_to(map) # blue

    # adding automatic zoom to last df
    sw = locations_df[['lat', 'lon']].min().values.tolist()
    ne = locations_df[['lat', 'lon']].max().values.tolist()

    map.fit_bounds([sw, ne], padding=(1,1), max_zoom=10)


# render Folium map in Streamlit
st_data = st_folium(map, width=2000, height=600)
