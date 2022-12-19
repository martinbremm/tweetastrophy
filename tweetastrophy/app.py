import streamlit as st
import folium
from streamlit_folium import st_folium
from predict import get_prediction
from map import create_map
from preprocessing import text_preprocessing

# configuring streamlit layout
st.set_page_config(page_title='Tweetastrophy', page_icon=':tada:', layout='wide')

# initializing session state
if 'txt' not in st.session_state:
    st.session_state['texts'] = []
if 'pred' not in st.session_state:
    st.session_state['predictions'] = []

# function to update session state
def updating_session_state():
    # creating text archive of all the txts
    st.session_state['texts'].append(st.session_state['txt'])
    st.session_state['predictions'].append(st.session_state['pred'])

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

# logo and text input in sidebar
with st.sidebar:
    a, b = st.columns([1, 20])
    with a:
        st.text("")
        st.image("tweetastrophy/twitter_logo.png", width=50)
    with b:
        st.title("Tweetastrophy")

    st.text("")
    with st.container() :
        st.info('Enter your tweet here 👇🏼 !!')
        txt = st.text_area(label='', placeholder='. . .', key='txt')

    # creating prediction value
    prediction = get_prediction(txt)
    st.session_state['pred'] = prediction

    # preprocessing text
    txt = text_preprocessing(txt)

    st.write(st.session_state)

    st.button(label='Predict', on_click = updating_session_state)

    st.write(st.session_state)

# creating prediction container
prediction_container = st.container()
col1, col2 = st.columns([8,17])

# css config
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(hide_menu, unsafe_allow_html=True)

local_css("tweetastrophy/config.toml")

# prediction output
if prediction == 'The tweet is Disaster Tweet':
    with col1:
        st.markdown('<p class="big-font"> Tweet refers to real disaster &#9888;&#65039; </p>', unsafe_allow_html=True)

elif prediction == 'The tweet is Non Disaster Tweet':
    with col1:
        st.markdown('<p class="big-font"> Tweet does not refer to a disaster &#x2705;</p>', unsafe_allow_html=True)




# map creation
if txt == "elon musk":
    st.image("tweetastrophy/elon_meme.png")

elif st.session_state['predictions']:
    # adding map based on the previous texts the person has entered
    create_map(st.session_state['texts'], st.session_state['predictions'])

else:
    st.markdown('<p class="big-font">Waiting for your tweet.. &#128564; </p>', unsafe_allow_html=True)



# clearing invalid entries from session state
if "" in st.session_state['texts']:
    st.session_state['texts'].remove("")
if "" in st.session_state['predictions']:
    st.session_state['predictions'].remove("")
