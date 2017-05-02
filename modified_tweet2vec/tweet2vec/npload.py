import numpy as np
import csv
import sys
def main(args):
    infile = args[0]
    preprocessed_file = args[1]
    outfile = args[2]
    res = np.load(infile)
    print res
    with open(preprocessed_file, 'rU') as csvfile:
        emoji = csv.reader(csvfile, delimiter=',', quotechar="|")
        writer = csv.writer(open(outfile, "w"), delimiter=';')
        ###Key - Emoji URL, Value - Vector embeddings
        for j,k in zip(emoji, res):
            writer.writerow([j[1], str(k.tolist()).strip('[]')])
if __name__ == '__main__':
    main(sys.argv[1:])
