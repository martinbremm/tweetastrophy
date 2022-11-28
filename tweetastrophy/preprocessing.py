import string
import re

from tweetastrophy.get_data import get_data

data = get_data()

## KEYWORD HANDLING

def preprocessing(data):
    ### KEYWORDS

    # handling NaN in keyword
    data["keyword"] = data["keyword"].fillna("")

    data["keyword"] = data['keyword'].str.replace("%20", " ")

    # adding hashtags to keywords
    data["keyword"] + data["text"].apply(lambda x: " ".join(re.findall("#(\w+)", x)).lower())


    ### TEXT

    data["punctuation"] = data["text"].apply(lambda sentence: "".join([char for char in sentence if char in string.punctuation]))

    data["wordcount"] = data["text"].apply(lambda x: len(x.split()))
