
#imports
from get_data import get_data
from preprocessing import preprocessing, tokenize_text, vectorization
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def train_model():
    #get data
    train_data, test_data = get_data(drop_location=True)

    #preprocess
    processed_train_data = preprocessing(train_data)

    #vectorization pipeline
    model = Pipeline([('Vectors', CountVectorizer(binary=True, ngram_range=(1,2))),
                        ('tfidf', TfidfTransformer()),
                        ('NB', MultinomialNB(alpha=0.55))])

    # fitting
    model.fit(processed_train_data['text'].values, processed_train_data["target"].values)

    return model
