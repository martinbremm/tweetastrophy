
#imports

from get_data import get_data
from preprocessing import preprocessing, tokenize_text
import joblib




def get_prediction(text):

    model = joblib.load('pretrained_model.joblib')

    if text == '':
        return ''
    else:
        predicted = model.predict([text])[0]

        if predicted == 1:
            return "The tweet is Disaster Tweet"
        else:
            return "The tweet is Non Disaster Tweet"
