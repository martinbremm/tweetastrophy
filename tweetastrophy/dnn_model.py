# dependencies
import tensorflow as tf
import numpy as np
import sklearn
from sklearn import metrics
import transformers
from transformers import TFRobertaForSequenceClassification, RobertaTokenizer
import json
import matplotlib.pyplot as plt
import random
import seaborn as sn

# import custom methods
from get_data import get_data
from preprocessing import preprocessing

train_data, test_data = get_data(drop_location=True)
train_data = preprocessing(train_data)
test_data = preprocessing(test_data)

X_train = train_data.drop(["keyword", "target"], axis=1)["text"].tolist()
X_test = test_data.drop("keyword", axis=1)["text"].tolist()

y_train = train_data[["target"]]


# tokenizing
tokenizer = RobertaTokenizer.from_pretrained('roberta-base') # Tokenizer
X_train_token = tokenizer(X_train, padding=True, truncation=True, return_tensors='tf')["input_ids"] #Tokenized text
X_test_token = tokenizer(X_test, padding=True, truncation=True, return_tensors='tf')["input_ids"] #Tokenized text



# model intitation
model = TFRobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=2) # 2 labels
# model compilation
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss='binary_crossentropy',
    metrics='accuracy',
    )

# model training
history=model.fit(x=X_train_token, y=y_train,
                  batch_size=128,
                  validation_split=0.1, epochs=6, verbose=1)

# saving weights
weight_dir = "../model_weights"
model.save_weights("".join([weight_dir, '/saved_weights.h5']))
