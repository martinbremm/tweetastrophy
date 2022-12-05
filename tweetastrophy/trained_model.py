
#imports
from get_data import get_data
from preprocessing import preprocessing, tokenize_text, vectorization
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB



def train_model():
    #get data
    train_data, test_data = get_data(drop_location=True)

    #preprocess
    processed_train_data = preprocessing(train_data)

    #tokenize
    tokenized_train_no_stopwords = tokenize_text(processed_train_data, remove_stopwords=True)

    #vectorize
    vectorizer = vectorization(tokenized_train_no_stopwords, fit=True)

    #model
    model = MultinomialNB(alpha=0.55)

    #fitting
    model.fit(vectorizer, processed_train_data["target"])

    return model
