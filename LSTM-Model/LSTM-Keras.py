# LSTM model for emoji recommendation for tweets
# Written by: Radha Krishnan Vinayagam

import numpy
from keras.layers import Dense, LSTM
from keras.layers.embeddings import Embedding
from keras.models import Sequential
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger
import pandas as pd
from sklearn.model_selection import train_test_split

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
numpy.set_printoptions(threshold='nan')

tweets = []
labels = []
#each tweet will uniformly have 140 chars
max_review_length = 140

#read data
with open("input2L.csv") as f:
    for l in f:
        tweet, label, search = l.strip().split(",")
        # tweets.append(tweet)
        # for char level encoding
        tweets.append(" ".join(list(tweet)))
        labels.append(label)

print "Total tweets:", len(tweets)

#to convert string labels to integer numbers
enc_labels = pd.Series(labels)
fact_labels = pd.factorize(enc_labels)
num_classes = len(fact_labels[1])

#to tokenize x and y
tokenizer = Tokenizer(filters="")
tokenizer.fit_on_texts(tweets)
X = tokenizer.texts_to_sequences(tweets)
X = sequence.pad_sequences(X, maxlen=max_review_length)
Y = np_utils.to_categorical(fact_labels[0], len(set(fact_labels[0])))

top_words = len(tokenizer.word_index) + 1
print "top_words:",top_words
print "num_classes:",num_classes

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=seed)

# create the model
embedding_vector_length = 50
model = Sequential()
model.add(Embedding(top_words, embedding_vector_length, input_length=max_review_length))
model.add(LSTM(150, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['top_k_categorical_accuracy'])
print(model.summary())

# checkpoint
filepath="weights-2L-best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
earlystopping = EarlyStopping(monitor='val_loss', patience=0, verbose=0, mode='auto')
csv_logger = CSVLogger('training2L.log')
callbacks_list = [checkpoint, earlystopping, csv_logger]
result = model.fit(X_train, y_train, validation_split=0.1, epochs=50, batch_size=32, callbacks=callbacks_list, verbose=1)
print(result.history)

#Final evaluation of the model
scores = model.evaluate(X_test, y_test, batch_size=32, verbose=0)
print("Accuracy: %.2f%%" % (scores[1] * 100))

# serialize model to JSON
model_json = model.to_json()
with open("model2L.json", "w") as json_file:
    json_file.write(model_json)
