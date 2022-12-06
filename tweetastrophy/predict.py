
#imports

from preprocessing import preprocessing
import joblib



def get_prediction(text):

    model = joblib.load('./tweetastrophy/trained_model.joblib')

    if text == '':
        return ''
    else:
        # preprocessing raw input text
        text = preprocessing(text)

        predicted = model.predict([text])[0]

        if predicted == 1:
            return "The tweet is Disaster Tweet"
        else:
            return "The tweet is Non Disaster Tweet"
