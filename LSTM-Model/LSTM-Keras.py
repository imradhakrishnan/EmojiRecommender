# LSTM for emoji recommendation for tweets
import numpy
from keras.layers import Dense, LSTM, Dropout
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.models import Sequential
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
numpy.set_printoptions(threshold='nan')

tweets = []
labels = []
#each tweet will uniformly have 140 chars
max_review_length = 140

with open("input30k.csv") as f:
    for l in f:
        tweet, label, search = l.strip().split(",")
        #tweets.append(tweet)
        #for char level encoding
        tweets.append(" ".join(list(tweet)))
        labels.append(label)

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
print top_words

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.02, random_state=seed)

#for single dimensional output
# y_train = numpy.reshape(y_train,(len(y_train), 1))
# y_test = numpy.reshape(y_test, (len(y_test), 1))

# create the model
embedding_vector_length = 128
model = Sequential()
model.add(Embedding(top_words, embedding_vector_length, input_length=max_review_length))
# model.add(Conv1D(filters=128, kernel_size=3, padding='same', activation='relu'))
# model.add(MaxPooling1D(pool_size=2))
model.add(LSTM(300, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['top_k_categorical_accuracy'])
print(model.summary())
result = model.fit(X_train, y_train, validation_split=0.33, epochs=50, batch_size=64, verbose=2)
print(result.history)

#Final evaluation of the model
scores = model.evaluate(X_test, y_test, batch_size=64, verbose=0)
print("Accuracy: %.2f%%" % (scores[1] * 100))
# cvscores.append(scores[1] * 100)

# print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))

# print(scores)
# print("training output")
# print(y_test)