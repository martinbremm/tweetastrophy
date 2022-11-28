import string
import re

from tweetastrophy.get_data import get_data

train_data, test_data = get_data()

## KEYWORD HANDLING

def preprocessing(train_data):
    ### KEYWORDS

    # handling NaN in keyword
    train_data["keyword"] = train_data["keyword"].fillna("")

    train_data["keyword"] = train_data['keyword'].str.replace("%20", " ")

    # adding hashtags to keywords
    train_data["keyword"] + train_data["text"].apply(lambda x: " ".join(re.findall("#(\w+)", x)).lower())

    #cleaning urls

    train_data['text'] = train_data['text'].apply(lambda x: re.sub('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
                                                       '', x))


    ### TEXT
    train_data['text'] = train_data['text'].apply(lambda x: x.lower())

    #strip data
    train_data['text'] = train_data['text'].str.strip()

    #remove digits
    train_data['text'] = train_data['text'].apply(lambda x: ''.join(i for i in x if i not in string.digits))

    #remove punctuations

    train_data['text'] = train_data['text'].apply(lambda x: ''.join(i for i in x if i not in string.punctuation))

    return train_data
