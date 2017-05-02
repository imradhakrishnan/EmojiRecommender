import csv
import re
import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
# nltk.download()
stop_words = set(stopwords.words("english"))
infile = sys.argv[1]
outfile = sys.argv[2]
csv.field_size_limit(sys.maxsize)
# -*- coding: utf-8 -*-
def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

with open(infile, 'rU') as csvfile:
  data = csv.reader(csvfile, delimiter=',', quotechar="|")
  processed_data =[]
  just_tweets = []
  for row in data:
      row_len = len(row)
      if(row_len > 1 and "twemoji.maxcdn" in row[1]):
          row[0] = row[0].strip('\"')
          row[0] = ''.join([i for i in row[0] if not i.isdigit()])
          row[0] =  re.sub(r'[^\x00-\x7f]','', row[0])
          row[0] =  re.sub(r'\x1b','', row[0])
          row[0] = word_tokenize(row[0])
          row[0] = filter(lambda x: x not in string.punctuation, row[0])
          row[0] = filter(lambda x: x not in stop_words, row[0])
        #   print row[0]
          tweet = ""
          for word in row[0]:
              tweet = tweet + " " + word
        #   print tweet
          if(len(tweet) > 5 and row_len > 3):
             just_tweets.append([tweet])
             emoji_set = set()
             for i in range(1, row_len - 1):
                row[i] = row[i].strip('\"')
                emoji_set.add(row[i])
             for emoji in emoji_set:
                new_row = [tweet, emoji, row[row_len - 1]]
                processed_data.append(new_row)
          else:
            if(len(row) == 3):
                processed_data.append([tweet, row[1], row[2]])

with open(outfile, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(processed_data)
