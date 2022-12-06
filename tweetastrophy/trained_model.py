from get_data import get_data
from preprocessing import train_preprocessing
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
# import joblib


def train_model():
    #get data
    train_data, test_data = get_data(drop_location=True)

    #preprocess
    processed_train_data = train_preprocessing(train_data)

    #vectorization pipeline
    model = Pipeline([('Vectors', CountVectorizer(binary=True, ngram_range=(1,2), stop_words="english")),
                        ('tfidf', TfidfTransformer()),
                        ('NB', MultinomialNB(alpha=0.55))])

    # fitting
    model.fit(processed_train_data['text'].values, processed_train_data["target"].values)

    # joblib.dump(model, "./tweetastrophy/trained_model.joblib")

    return model

model = train_model()
