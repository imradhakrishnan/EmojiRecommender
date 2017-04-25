import csv
import operator
import sys
from scipy import spatial
infile = sys.argv[1]
outfile = sys.argv[2]
testvec = sys.argv[3]
truevalues = sys.argv[4]
emojisimilarities = {}
def getSimilarEmojis(u, k):
    vec1 = map(lambda x: float(x), u)
    with open(infile, "rb") as file:
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

def countSimilarEmojis(l1, l2):
    origlist = l1
    recommset = set(l2)
    count = 0
    for e in origlist:
        if e in recommset:
            count += 1
    print count
    return count

def getSimilarEmojisWrapper():
    k = 5
    emojirecommendations = {}
    writer = csv.writer(open(outfile, "w"))
    with open(testvec, "rb") as file:
        reader = csv.reader(file, delimiter=';')
        count = 0
        for row in reader:
            vec = map(float, row[0].split(','))
            similar = getSimilarEmojis(vec, k)
            print(similar)
            emojirecommendations[count] = similar
            count += 1
            #if count == 5:
            #    break

    with open(truevalues, "rb") as file:
        origdata = csv.reader(file, delimiter=',')
        count = 0
        for row in origdata:
            print row[1]
            numsimilaremojis = countSimilarEmojis(row[1], emojirecommendations[count])
            writer.writerow([row, emojirecommendations[count], numsimilaremojis])
            count += 1
            #if count == 5:
            #    break
    # with open("test_tweet_embeddings.csv", "rb") as file:
    #     reader = csv.reader(file, delimiter=';')
    #     with open("test_preprocessed_tweet_2.csv", "rb") as original:
    #         original_data = csv.reader(original, delimiter=',')
    #         #for row in original_data:
    #         #    print row
    #         for row, original_row in zip(reader, original_data):
    #             vec = map(float, row[0].strip('[,]').split(','))
    #             similar = getSimilarEmojis(vec, k)
    #             writer.writerow([original_row, similar])

getSimilarEmojisWrapper()
