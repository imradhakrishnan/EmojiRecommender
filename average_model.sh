#!/usr/bin/env bash
cd /home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/tweet2vec/ &&
python data_process.py '/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/preprocessed_tweet_1.csv home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/input.csv' '/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/preprocessed_tweet_1.csv' &&
cd /home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/misc/ &&
python preprocess.py '/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/preprocessed_tweet_1.csv' '/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/preprocessed_tweet_2.csv' &&
cd /home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/tweet2vec/ &&
./tweet2vec_encoder.sh &&
python npload.py '/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/tweet2vec/result/embeddings.npy' '/../data/preprocessed_tweet_2' '/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/tweet_embeddings.csv'&&
cd /home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/RecommendEmojis/ &&
python EmojiEmbeddings.py "/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/tweet_embeddings.csv" &&
python EmojiRecommender.py "/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/emoji2vec.csv" "/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/Test_RecommendedEmojis.csv" "/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/test_tweet_embeddings.csv" "/home/jagathshree/Documents/files/Spring 2017/DBMS/Project/EmojiRecommender/modified_tweet2vec/data/test_preprocessed_tweet_2.csv"
