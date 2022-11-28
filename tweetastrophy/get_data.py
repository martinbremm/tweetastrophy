import pandas as pd
def get_data():
    train_data = pd.read_csv("raw_data/train.csv")
    train_data = train_data.drop(columns="id")
    test_data = pd.read_csv("raw_data/test.csv")
    test_data = test_data.drop(columns="id")

    return train_data, test_data
