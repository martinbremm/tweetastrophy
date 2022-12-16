import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from predict import get_prediction
from preprocessing import text_preprocessing

from location import create_location

@st.experimental_memo(suppress_st_warning=True)
def create_map(text_archive, prediction):

    # initialize empty map if no input or no previous input
    map = folium.Map(location=[0,0],
                    tiles="cartodbpositron",
                    zoom_start=3, control_scale=True)

    if not text_archive:
        return  st_folium(map, width=1200, height=600, returned_objects=[])

    elif type(text_archive) == list:
        if text_archive[-1] == "":
            return  st_folium(map, width=1200, height=600, returned_objects=[])

    else:
        text_df = pd.DataFrame.from_dict(data={"text": text_archive})

        locations_df = create_location(text_df)

        df = pd.concat([text_df, locations_df], axis=1)

        # creating basic map in folium
        map = folium.Map(location=[locations_df.lat.mean(), locations_df.lon.mean()],
                        tiles="cartodbpositron",
                        zoom_start=5, min_zoom=3, control_scale=True)

        # mapping circles to df in DataFrame
        df_dict = df.to_dict("records")

        st.write(df_dict)

        # looping over combined df
        for idx, row in enumerate(df_dict):

            # determining the color of the circle
            if prediction[idx] == "The tweet is Disaster Tweet":
                color = "#EE4B2B" # red
            elif prediction[idx] == "The tweet is Non Disaster Tweet":
                color = "#008000" # green

            # checking for rows without coordinates
            if row["lat"] == 0.0 or row["lon"] == 0.0:
                map = folium.Map(location=[0,0],
                    tiles="cartodbpositron",
                    zoom_start=3, control_scale=True)

                continue
                #return  st_folium(map, width=1200, height=600, returned_objects=[])

            # city data available
            elif row["city"] != "Unknown":
                if row["size"] == "Not Found":
                    radius=10000
                else:
                    radius=row["size"]

                folium.Circle(location=[row["lat"], row["lon"]], radius=radius, popup=row["city"],
                                    color=color, fill=True, fill_color=color).add_to(map)

            elif (row["region"] != "Unknown") & (row["city"] == "Unknown"):
                if row["size"] == "Not Found":
                    radius=660000
                else:
                    radius=row["size"]

                folium.Circle(location=[row["lat"], row["lon"]], radius=radius, popup=row["region"],
                                    color=color, fill=True, fill_color=color).add_to(map)

            # country data available
            elif (row["country"] != "Unknown") & (row["region"] == "Unknown") & (row["city"] == "Unknown"):
                if row["size"] == "Not Found":
                    radius=660000
                else:
                    radius=row["size"]

                folium.Circle(location=[row["lat"], row["lon"]], radius=660000, popup=row["country"],
                                    color=color, fill=True, fill_color=color).add_to(map)

        # adding automatic zoom to last df
        sw = locations_df[['lat', 'lon']].min().values.tolist()
        ne = locations_df[['lat', 'lon']].max().values.tolist()

        map.fit_bounds([sw, ne], padding=(1,1), max_zoom=8)

        st.write("Done")

        return st_folium(map, width=1200, height=1200)
