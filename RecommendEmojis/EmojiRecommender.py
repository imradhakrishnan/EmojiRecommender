import csv
import operator
import sys
from scipy import spatial
emojisimilarities = {}
def getSimilarEmojis(infile, u, k):
    vec1 = map(lambda x: float(x), u)
    with open(infile, "rb") as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            vec2 = map(float, row[1].strip('[,]').split(','))
            emojisimilarities[row[0]] = 1 - spatial.distance.cosine(vec1, vec2)

    sorted_emojis = sorted(emojisimilarities.items(), key=operator.itemgetter(1))
    sorted_emojis.reverse()

    # count = 0
    # print len(sorted_emojis)
    # recommended_emojis = []
    # while count < k:
    #     recommended_emojis.insert(count, sorted_emojis[count][0])
    #     count += 1


    # return recommended_emojis
    return sorted_emojis

def countSimilarEmojis(l1, l2):
    origlist = l1
    emojis = []
    for element in l2:
        emojis.append(element[0])
    # print emojis
    # recommset = set(l2)
    # count = 0
    # for e in origlist:
    #     if e in recommset:
    #         count += 1
    # print count
    # return count

    try:
        isTop5 = 0
        rank = emojis.index(l1)
        if rank in range(0, 5):
            # print(rank)
            isTop5 = 1
        # return emojis.index(l1)
        return [rank, isTop5]
    except ValueError:
        # return -1
        return [-1, isTop5]

def getSimilarEmojisWrapper(args):
    infile = args[0]
    outfile = args[1]
    testvec = args[2]
    truevalues = args[3]
    k = 5
    emojirecommendations = {}
    top5 = 0
    accuracy = 0
    total_count = 0
    writer = csv.writer(open(outfile, "w"))
    with open(testvec, "rb") as file:
        reader = csv.reader(file, delimiter=';')
        count = 0
        for row in reader:
            vec = map(float, row[1].split(','))
            sorted_emojis = getSimilarEmojis(infile,vec, k)
            # similar = getSimilarEmojis(vec, k)
            # print(similar)
            emojirecommendations[count] = sorted_emojis
            count += 1
    with open(truevalues, "rb") as file:
        origdata = csv.reader(file, delimiter=',')
        count = 0

        for row in origdata:
            numsimilaremojis = countSimilarEmojis(row[1], emojirecommendations[count])
            # print(numsimilaremojis)
            # writer.writerow([row, emojirecommendations[count], numsimilaremojis])
            writer.writerow([row[1], numsimilaremojis[0]])
            count += 1
            if(numsimilaremojis[1] == 1):
                top5 += 1
        total_count = count
    # print top5
    # print total_count
    accuracy = 100*top5/total_count
    print accuracy

def main(args):
    getSimilarEmojisWrapper(args)
if __name__ == '__main__':
    main(sys.argv[1:])
