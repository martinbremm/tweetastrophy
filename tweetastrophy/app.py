import streamlit as st
import folium
from streamlit_folium import st_folium
from predict import get_prediction
from map import create_map
from preprocessing import text_preprocessing

# configuring streamlit layout
st.set_page_config(page_title='Tweetastrophy', page_icon=':tada:', layout='wide')

@st.experimental_memo(suppress_st_warning=True)
def mapping_app():

    # initializing session state
    if 'txt' not in st.session_state:
        st.session_state['txt'] = []
    if 'pred' not in st.session_state:
        st.session_state['pred'] = []

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
            #st.markdown('<p class="mid-font"> Enter your tweet here 👇🏼 !!</p>', unsafe_allow_html=True)
            st.info('Enter your tweet here 👇🏼 !!')
            txt = st.text_area('', placeholder='. . .')
            st.button('Predict')

    # creating prediction container
    prediction_container = st.container()
    col1, col2 = st.columns([8,17])

    # creating prediction value
    prediction = get_prediction(txt)

    # css config
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(hide_menu, unsafe_allow_html=True)

    local_css("tweetastrophy/config.toml")

    # preprocessing text
    txt = text_preprocessing(txt)

    # creating text archive of all the txts
    st.session_state['txt'].append(txt)
    st.session_state['pred'].append(prediction)

    # prediction output
    if prediction == 'The tweet is Disaster Tweet':
        with col1:
            st.markdown('<p class="big-font"> Tweet refers to real disaster &#9888;&#65039; </p>', unsafe_allow_html=True)

    elif prediction == 'The tweet is Non Disaster Tweet':
        with col1:
            st.markdown('<p class="big-font"> Tweet does not refer to a disaster &#x2705;</p>', unsafe_allow_html=True)

    st.write(st.session_state)


    # map creation
    if txt == "elon musk":
        st.image("tweetastrophy/elon_meme.png")

    elif st.session_state['pred']:
        # adding map based on the previous texts the person has entered
        create_map(st.session_state['txt'], st.session_state['pred'])

    else:
        st.markdown('<p class="big-font">Waiting for your tweet.. &#128564; </p>', unsafe_allow_html=True)
        create_map(st.session_state['txt'], st.session_state['pred'])


    # clearing invalid entries from session state
    if "" in st.session_state['txt']:
        st.session_state['txt'].remove("")
    if "" in st.session_state['pred']:
        st.session_state['pred'].remove("")

    # clearing streamlit cache
    #create_map.clear()

mapping_app()
