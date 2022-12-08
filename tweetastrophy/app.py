import streamlit as st
from streamlit_folium import st_folium
from predict import get_prediction
from map import create_map
import folium


if 'txt' not in st.session_state:
	st.session_state.txt = [""]

def text_adding():
    st.write(st.session_state)


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
    txt = st.text_area('Enter your tweet here 👇🏼', '', on_change=text_adding())
    st.session_state.txt.append(txt)

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


# creating text archive of all the txts

if prediction:
    # adding map based on the previous texts the person has entered
    #create_map(st.session_state.txt, prediction)
    st.write("map")

else:
    map = folium.Map(location=[0,0],
                    tiles="cartodbpositron",
                    zoom_start=3, control_scale=True)
