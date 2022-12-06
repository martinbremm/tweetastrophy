from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline


import string
import re

## KEYWORD HANDLING


def preprocessing(df):
    ### KEYWORDS

    # handling NaN in keyword
    df["keyword"] = df["keyword"].fillna("")

    df["keyword"] = df['keyword'].str.replace("%20", " ")

    # adding hashtags to keywords
    df['keyword'] = df["keyword"] + df["text"].apply(lambda x: " ".join(re.findall("#(\w+)", x)).lower())

    ### TEXT

    # lower case
    df['text'] = df['text'].apply(lambda x: x.lower())

    #strip data
    df['text'] = df['text'].str.strip()

    #cleaning urls
    df['text'] = df['text'].apply(lambda x: re.sub('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
                                                       '', x))
    #remove emails
    df['text'] = df['text'].apply(lambda x: re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)',"", x))

    #clean username
    df['text'] = df['text'].apply(lambda x: re.sub('@[^\s]+','', x))

    #remove digits
    df['text'] = df['text'].apply(lambda x: ''.join(i for i in x if i not in string.digits))

    #remove punctuations
    df['text'] = df['text'].apply(lambda x: ''.join(i for i in x if i not in string.punctuation))

    return df


def tokenize_text(df, remove_stopwords=False):

    df['Tokenized'] = df['text'].apply(word_tokenize)

    # remove unreadable char
    df['Tokenized'] = df['Tokenized'].apply(lambda x: [word.encode('ascii','ignore').decode('ascii')for word in x])

    if remove_stopwords:
        stop = stopwords.words('english')
        df['Tokenized'] = df['Tokenized'].apply(lambda x: [i for i in x if i not in stop])

        return df

    return df

"""def vectorization(df, fit=False):
    #pipeline

    pipe = Pipeline([('Vectors', CountVectorizer(binary=True, ngram_range=(1,2))),
                        ('tfidf', TfidfTransformer())])
    if fit == True:
        pipe = pipe.fit(df)
        transformed_df = pipe.transform(df)
        return transformed_df
    else:
        transformed_df = pipe.transform(df)
        return transformed_df"""
