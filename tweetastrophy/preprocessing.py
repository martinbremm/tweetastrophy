import string
import re

## KEYWORD HANDLING

def train_preprocessing(df):
    ### KEYWORDS

    # handling NaN in keyword
    df["keyword"] = df["keyword"].fillna("")

    df["keyword"] = df['keyword'].str.replace("%20", " ")

    # adding hashtags to keywords
    df['keyword'] = df["keyword"] + df["text"].apply(lambda x: " ".join(re.findall("#(\w+)", x)).lower())

    ### TEXT

    df["text"] = df["text"].apply(lambda row: text_preprocessing(row))

    return df

def text_preprocessing(text):
    ### TEXT

    # lower case
    text = text.lower()

    #strip data
    text = text.strip()

    #cleaning urls
    text = re.sub('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
                                                       '', text)
    #remove emails
    text = re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)',"", text)

    #clean username
    text = re.sub('@[^\s]+','', text)

    #remove digits
    text = ''.join(i for i in text if i not in string.digits)

    #remove punctuations
    text = ''.join(i for i in text if i not in string.punctuation)

    return text

"""def tokenize_text(df, remove_stopwords=False):

    df['Tokenized'] = df['text'].apply(word_tokenize)

    # remove unreadable char
    df['Tokenized'] = df['Tokenized'].apply(lambda x: [word.encode('ascii','ignore').decode('ascii')for word in x])

    if remove_stopwords:
        stop = stopwords.words('english')
        df['Tokenized'] = df['Tokenized'].apply(lambda x: [i for i in x if i not in stop])

    return df

def vectorization(df, fit=False):
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
