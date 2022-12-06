
#imports
from get_data import get_data
from preprocessing import preprocessing, tokenize_text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def get_model():
    #get data
    train_data, test_data = get_data(drop_location=True)

    #preprocess
    processed_train_data = preprocessing(train_data)

    #tokenize
    tokenized_train_no_stopwords = tokenize_text(processed_train_data, remove_stopwords=True)

    #vectorize
    count_vectorizer = CountVectorizer(binary=True, ngram_range=(1,2))
    train_vectors_count = count_vectorizer.fit_transform(tokenized_train_no_stopwords['text'])

    #model
    model = MultinomialNB(alpha=0.55)

    #fitting
    model.fit(train_vectors_count, processed_train_data["target"])

    return model

def get_prediction(text):
    if text == '':
        return ''
    else:
        #get data
        train_data, test_data = get_data(drop_location=True)

        #preprocess
        processed_train_data = preprocessing(train_data)

        #pipeline
        pipe = Pipeline([('Vectors', CountVectorizer(binary=True, ngram_range=(1,2))),
                        ('tfidf', TfidfTransformer()),
                        ('NB', get_model())])

        pipe.fit(processed_train_data['text'].values, processed_train_data["target"].values)

        predicted = pipe.predict([text])[0]

        if predicted == 1:
            return "The tweet is Disaster Tweet"
        else:
            return "The tweet is Non Disaster Tweet"
