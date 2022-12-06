
#imports
from get_data import get_data
from preprocessing import preprocessing, tokenize_text
import emoji
import joblib




def get_prediction(text):

    model = joblib.load('pretrained_model.joblib')

    if text == '':
        return ''
    else:
        predicted = model.predict([text])[0]

        if predicted == 1:
            return emoji.emojize("The tweet is Disaster Tweet :exclamation:")
        else:
            return emoji.emojize("The tweet is Non Disaster Tweet :white_check_mark:")
