import csv
import operator
from scipy import spatial

emojisimilarities = {}
def getSimilarEmojis(u, k):
    vec1 = map(lambda x: float(x), u)
    with open("emoji2vec.csv", "rb") as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            vec2 = map(float, row[1].strip('[,]').split(','))
            emojisimilarities[row[0]] = 1 - spatial.distance.cosine(vec1, vec2)

    sorted_emojis = sorted(emojisimilarities.items(), key=operator.itemgetter(1))
    sorted_emojis.reverse()

    count = 0
    recommended_emojis = []
    while count < k:
        recommended_emojis.insert(count, sorted_emojis[count][0])
        count += 1
    return recommended_emojis

def getSimilarEmojisWrapper():
    k = 5
    writer = csv.writer(open("RecommendedEmojis.csv", "w"), delimiter=';')
    with open("TweetEmbeddings.csv", "rb") as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            vec = map(float, row[0].strip('[,]').split(','))
            writer.writerow(getSimilarEmojis(vec, k))

getSimilarEmojisWrapper()
