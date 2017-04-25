import csv
import sys
infile = sys.argv[1]
emojidict = {}
emojicount = {}

def add_vectors(v1, v2):
    return [v1 + v2 for v1, v2 in zip(v1,v2)]

def average_vectors():
    for k,v in emojicount.items():
        emojidict[k] = [(1/float(v))*x for x in emojidict[k]]

with open(infile, 'rb') as file:
    reader = csv.reader(file, delimiter=';', quotechar='|')
    for row in reader:
        vec = map(float, row[1].strip('[,]').split(","))
        if row[0] not in emojidict:
            emojidict[row[0]] = vec
            emojicount[row[0]] = 1
        else:
            emojidict[row[0]] = add_vectors(vec, emojidict[row[0]])
            emojicount[row[0]] += 1
    average_vectors()
    writer = csv.writer(open("/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/emoji2vec.csv", "w"), delimiter =';')
    for k,v in emojidict.items():
        writer.writerow([k,v])
