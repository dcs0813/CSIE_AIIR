# -*- coding: utf-8 -*-
#
# AIIR Final Project 01 :: 載入預訓練好的 word2vec 作相關字詞搜尋
#

import os
import sys
import pandas as pd
import pickle

from gensim.models import word2vec
from nltk.metrics import edit_distance

#======================================================================================================
### 預定義相關變數
#======================================================================================================
# 載入預訓練的 word2vec 模型
model = word2vec.Word2Vec.load("./w2v_model/word2vec_skipgram_dim_200_train_300.model")

# 定義搜尋關鍵字
queryText01 = 'COVID19'
queryText02 = 'mRNA'

#======================================================================================================
### 函數定義 :: 詞向量最相近的前 N 筆 :: 單筆
#======================================================================================================
def most_similar_1txt( w2v_model, queryText, topn ):
    try:
        similar_words = pd.DataFrame( w2v_model.wv.most_similar( queryText, topn = topn ), columns = [queryText, 'cos'] )
    except:
        similar_words = "N/A"
    
    return similar_words

#======================================================================================================
### 函數定義 :: Query Expansion
#======================================================================================================
def query_expansion( queryText ):
    # 定義 edit distance 值
    eDistance = 2
    queryExpansion = []

    # 透過預訓練的 word2vec model 取得搜尋關鍵字的相關字詞
    similar_words = most_similar_1txt( model, queryText, 10 )

    # 先將原搜尋關鍵字置入 queryExpansion 的 list 中
    queryExpansion.append( queryText )

    # 將相關字詞逐一作 edit distance 的檢查再置入 queryExpansion 中 :: 統一都轉成小寫 來作比對
    for word in similar_words[queryText]:
        if edit_distance( queryText.lower(), word.lower() ) <= eDistance:
            queryExpansion.append( word )

    return queryExpansion

#======================================================================================================
### 函數定義 :: 關鍵字搜尋
#======================================================================================================
def keyWordsSearch( queryContent, queryText ):
    matchedResult = []
    for content in queryContent:
        # 對內容作特定字詞搜尋
        result = [i for i in range( len( content ) ) if content.startswith( queryText, i ) ]
        if result != []:
            matchedResult.append( content )

    return matchedResult

#======================================================================================================
### 執行
#======================================================================================================
queryExpansion01 = query_expansion( queryText01 )
queryExpansion02 = query_expansion( queryText02 )

print(  )

sys.exit()
