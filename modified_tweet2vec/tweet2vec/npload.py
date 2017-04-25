import numpy as np
import csv
import sys
infile = sys.argv[1]
preprocessed_file = sys.argv[2]
outfile = sys.argv[3]
res = np.load(infile)
with open(preprocessed_file, 'rU') as csvfile:
    emoji = csv.reader(csvfile, delimiter=',', quotechar="|")
    writer = csv.writer(open(outfile, "w"), delimiter=';')
    ###Key - Emoji URL, Value - Vector embeddings
    for j,k in zip(emoji, res):
        writer.writerow([j[1], k])
