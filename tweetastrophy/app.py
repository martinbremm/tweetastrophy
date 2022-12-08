import streamlit as st
import folium
from streamlit_folium import st_folium
from predict import get_prediction
from map import create_map
from preprocessing import text_preprocessing

# initializing text archive
text_archive = []

st.set_page_config(page_title='Tweetastrophy', page_icon=':tada:', layout='wide')

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


with st.sidebar:
    a, b = st.columns([1, 20])
    with a:
        st.text("")
        st.image("tweetastrophy/twitter_logo.png", width=50)
    with b:
        st.title("Tweetastrophy")

    st.text("")
    with st.container() :
        #st.markdown('<p class="mid-font"> Enter your tweet here 👇🏼 !!</p>', unsafe_allow_html=True)
        st.info('Enter your tweet here 👇🏼 !!')
        txt = st.text_area('', placeholder='. . .')
        st.button('Predict')

# creating prediction value
prediction = get_prediction(txt)

prediction_container = st.container()
col1, col2 = st.columns([8,17])

# creating prediction value
prediction = get_prediction(txt)



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(hide_menu, unsafe_allow_html=True)

local_css("tweetastrophy/config.toml")

# preprocessing text
txt = text_preprocessing(txt)
# creating text archive of all the txts
text_archive.append(txt)

text_archive = list(set(text_archive))

if prediction == 'The tweet is Disaster Tweet':
    with col1:
        st.markdown('<p class="big-font"> Tweet is a disaster &#9888;&#65039; </p>', unsafe_allow_html=True)


elif prediction == 'The tweet is Non Disaster Tweet':
    with col1:
        st.markdown('<p class="big-font"> Tweet is not a disaster &#x2705;</p>', unsafe_allow_html=True)




if prediction:
    # adding map based on the previous texts the person has entered
    create_map(text_archive, prediction)

else:
    st.markdown('<p class="big-font">Waiting for your tweet.. &#128564; </p>', unsafe_allow_html=True)
    create_map(text_archive, prediction)

create_map.clear()
