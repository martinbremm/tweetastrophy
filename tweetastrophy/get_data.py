import pandas as pd
def get_data():
    data = pd.read_csv("raw_data/train.csv")
    data = data.drop(columns="id")
    return data
