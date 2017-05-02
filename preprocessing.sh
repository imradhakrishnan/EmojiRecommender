#!/usr/bin/env bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
cd modified_tweet2vec/tweet2vec/ &&
python data_process.py $parent_path'/modified_tweet2vec/data/input.csv' $parent_path'/modified_tweet2vec/data/input_preprocessed_1.csv' &&
cd $parent_path"/modified_tweet2vec/misc/" &&
python preprocess.py $parent_path'/modified_tweet2vec/data/input_preprocessed_tweet_1.csv' $parent_path'/modified_tweet2vec/data/input_preprocessed_2.csv'
