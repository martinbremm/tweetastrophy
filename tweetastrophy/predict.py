
from preprocessing import text_preprocessing
import joblib
import streamlit as st

@st.cache(allow_output_mutation=True)
def get_prediction(text):

    model = joblib.load('./tweetastrophy/trained_model.joblib')

    if text == '':
        return ''
    else:
        # preprocessing raw input text
        text = text_preprocessing(text)

        predicted = model.predict([text])[0]

        if predicted == 1:
            return "The tweet is Disaster Tweet"
        else:
            return "The tweet is Non Disaster Tweet"
