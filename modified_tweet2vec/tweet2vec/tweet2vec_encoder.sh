#!/bin/bash

# specify data file here
datafile="../data/test_preprocessed_tweet_2.csv"

# specify model path here
modelpath="best_model/"

# specify result path here
resultpath="result/"

mkdir -p $resultpath

# test
python encode_char.py $datafile $modelpath $resultpath
