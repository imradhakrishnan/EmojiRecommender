#!/bin/bash

# specify data file here
datafile="/home/jagathshree/Documents/files/Spring2017/DBMS/EmojiRecommender/modified_tweet2vec/data/sample_test_preprocessed_tweet_2.csv"

# specify model path here
modelpath="best_model/"

# specify result path here
resultpath="result/"

mkdir -p $resultpath

# test
python encode_char.py $datafile $modelpath $resultpath
