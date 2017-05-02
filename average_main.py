import subprocess
import csv
import numpy as np
import sklearn
import os
import sys
path = os.path.abspath(__file__)
mainpath = os.path.dirname(path)
sys.path.append(mainpath + '/modified_tweet2vec/tweet2vec/')
import encode_char as ec
import npload as npl
sys.path.append(mainpath + '/RecommendEmojis/')
import EmojiEmbeddings as ee
import EmojiRecommender as er
from sklearn.model_selection import KFold
#Call preprocessing - the shell script calls two preprocessing scripts
print "Start Preprocessing"
if subprocess.call("./preprocessing.sh") == 0:
    print "Done preprocessing"
    #Call script to embed tweets
    print "Begin encoding"
    inputpath = mainpath + "/modified_tweet2vec/data/input_preprocessed_2.csv"
    modelpath = mainpath + "/modified_tweet2vec/tweet2vec/best_model/"
    outputpath = mainpath + "/modified_tweet2vec/tweet2vec/result"
    args = []
    args.append(inputpath)
    args.append(modelpath)
    args.append(outputpath)
    ec.main(args)
    print "Done encoding"
    #Converts output of encoding (.npy) to .csv
    print "Begin converting .npy to .csv"
    npypath = mainpath + "/modified_tweet2vec/tweet2vec/result/embeddings.npy"
    prepath = mainpath + "/modified_tweet2vec/data/input_preprocessed_2.csv"
    csvpath = mainpath + "/modified_tweet2vec/data/embeddings.csv"
    nplargs = []
    nplargs.append(npypath)
    nplargs.append(prepath)
    nplargs.append(csvpath)
    npl.main(nplargs)
    print("Finished converting .npy to .csv")
    #Splits data for cross validation
    print "Start splitting data"
    embed_data = mainpath + "/modified_tweet2vec/data/embeddings.csv"
    with open(inputpath, "rb") as inputfile:
        inputdata = csv.reader(inputfile, delimiter=",")
        inputdata = np.asarray(list(inputdata))
        with open(embed_data, "rb") as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            data = list(data)
            kf = KFold(n_splits=5)
            kf.get_n_splits(data)
            i = 1
            indices = kf.split(data)
            print indices
            for train_index, test_index in indices:
                data_train = []
                data_test = []
                for ti in train_index:
                    data_train.append(data[ti])
                for test_i in test_index:
                    data_test.append(data[test_i])
                main_data_train, main_data_test = inputdata[train_index], inputdata[test_index]
                trainfile = mainpath + "/modified_tweet2vec/data/train"
                testfile = mainpath + "/modified_tweet2vec/data/test"
                trainfile = trainfile + str(i) + ".csv"
                testfile = testfile + str(i) + ".csv"
                main_trainfile = mainpath + "/modified_tweet2vec/data/main_train"
                main_testfile = mainpath + "/modified_tweet2vec/data/main_test"
                main_trainfile = main_trainfile + str(i) + ".csv"
                main_testfile = main_testfile + str(i) + ".csv"
                with open(trainfile, 'w') as traincsv:
                    writer = csv.writer(traincsv)
                    writer.writerows(data_train)
                with open(testfile, 'w') as testcsv:
                    writer = csv.writer(testcsv)
                    writer.writerows(data_test)
                with open(main_trainfile, 'w') as main_traincsv:
                    writer = csv.writer(main_traincsv)
                    writer.writerows(main_data_train)
                with open(main_testfile, 'w') as main_testcsv:
                    writer = csv.writer(main_testcsv)
                    writer.writerows(main_data_test)
                i += 1
    print "Done splitting"
    #Maps the embedding from the train set to the emoji corpus
    print "Begin emoji embedding"
    for i in range(1,6):
        train_data = mainpath + "/modified_tweet2vec/data/train"
        train_data = train_data + str(i) + ".csv"
        emoji_embed_output = mainpath + "/modified_tweet2vec/data/emoji_embeddings"
        emoji_embed_output = emoji_embed_output + str(i) + ".csv"
        emoji_embed_args = []
        emoji_embed_args.append(train_data)
        emoji_embed_args.append(emoji_embed_output)
        ee.main(emoji_embed_args)
        #Recommends emojis - does cosine similarity, ranking and accuracy calculation
        recommend_output =  mainpath + "/modified_tweet2vec/data/RecommendedEmojis"
        recommend_output = recommend_output + str(i) + ".csv"
        test_data = mainpath + "/modified_tweet2vec/data/test"
        test_data = test_data + str(i) + ".csv"
        main_testfile = mainpath + "/modified_tweet2vec/data/main_test"
        main_testfile = main_testfile + str(i) + ".csv"
        recommend_args = []
        recommend_args.append(emoji_embed_output)
        recommend_args.append(recommend_output)
        recommend_args.append(test_data)
        recommend_args.append(main_testfile)
        er.main(recommend_args)
print "end"
