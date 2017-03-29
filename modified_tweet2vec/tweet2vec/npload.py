import numpy as np
import csv
res = np.load('/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/tweet2vec/tweet2vec/result/embeddings.npy')
with open('/../data/preprocessed_tweet_2', 'rU') as csvfile:
    emoji = csv.reader(csvfile, delimiter=',', quotechar="|")
    writer = csv.writer(open("/../data/tweet_embeddings.csv", "w"), delimiter=';')
    ###Key - Emoji URL, Value - Vector embeddings
    for j,k in zip(emoji, res):
        writer.writerow([j[1], k])
