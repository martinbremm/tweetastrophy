import pandas as pd
def get_data(drop_location=False):
    train_data = pd.read_csv("../raw_data/train.csv")
    train_data = train_data.drop(columns="id")

    test_data = pd.read_csv("../raw_data/test.csv")
    test_data = test_data.drop(columns="id")

    if drop_location == True:
        train_data.drop(columns='location', inplace=True)
        test_data.drop(columns='location', inplace=True)

    return train_data, test_data
