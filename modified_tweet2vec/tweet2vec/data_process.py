import csv
import re
infile = sys.argv[1]
outfile = sys.argv[2]
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
          if(len(row[0]) > 5 and row_len > 3):
             just_tweets.append([row[0]])
             emoji_set = set()
             for i in range(1, row_len - 1):
                row[i] = row[i].strip('\"')
                emoji_set.add(row[i])
             for emoji in emoji_set:
                new_row = [row[0], emoji, row[row_len - 1]]
                processed_data.append(new_row)
          else:
            if(len(row) == 3):
                processed_data.append(row)

with open(outfile, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(processed_data)
