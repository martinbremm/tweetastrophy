import streamlit as st
from get_data import get_data
from preprocessing import preprocessing, tokenize_text
from model import get_model, get_prediction
import numpy as np
import pandas as pd

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
