# -*- coding: utf-8 -*-
#
# AIIR Final Project :: 載入預訓練好的 word2vec 作相關字詞搜尋
#

import os
import sys
import pandas as pd
import pickle
import time

from gensim.models import word2vec
from nltk.metrics import edit_distance
from rank_bm25 import BM25Okapi

#======================================================================================================
### 預定義相關變數
#======================================================================================================
# 載入預訓練的 word2vec 模型
model = word2vec.Word2Vec.load("../model/w2v_model/word2vec_skipgram_dim_200_train_300.model")

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
### 函數定義 :: 載入文件，產生搜尋基底內容
#======================================================================================================
def getQueryContent():
    
    # 讀取原始檔案
    df = pd.read_csv( "../data/metadata_oct19.csv", encoding='utf8', low_memory=False )

    # 只取 abstract 的部份
    content = df['abstract']

    # 去除 abstract 為 NaN 的部份
    content = content.dropna()

    # 取前 N 筆作為搜尋基底
    queryContent = content.head( 200 )

    return queryContent

#======================================================================================================
### 函數定義 :: 關鍵字搜尋
#======================================================================================================
def keyWordsSearch( queryContent, queryText ):
    matchedResult = []
    for text in queryText:
        for content in queryContent:
            # 對內容作特定字詞搜尋
            result = [i for i in range( len( content ) ) if content.startswith( text, i ) ]
            if result != []:
                matchedResult.append( content )

    return matchedResult

#======================================================================================================
### 執行
#======================================================================================================
# 讀取 & 建立搜尋基底
queryContent = getQueryContent()

# 記錄執行時間_開始
start_time = time.time()

# 對搜尋字詞作 query expansin
queryExpansion01 = query_expansion( queryText01 )
queryExpansion02 = query_expansion( queryText02 )



# 讀取預訓練的 bm25 模型
with open('../model/bm25_model/bm25_document_200', 'rb') as bm25ResultFile:
    bm25 = pickle.load( bm25ResultFile )

query = "covid-19"
tokenized_query = query.split(" ")

print( bm25.get_top_n( tokenized_query, queryContent, n=2 ) )


# 對文章內容作搜尋
#matchedResult01 = keyWordsSearch( queryContent, queryExpansion01 )

# 對文章內容作搜尋
#matchedResult02 = keyWordsSearch( matchedResult01, queryExpansion02 )

#print( len( matchedResult01 ) )

#======================================================================================================
### 計算執行時間
#======================================================================================================
end_time = time.time()
seconds = end_time - start_time

# 將執行時間轉換成「 時 : 分 : 秒 」的格式
m, s = divmod( seconds, 60 )
h, m = divmod( m, 60 )

print( '執行時間 :: ', "%d : %02d : %02d" % (h, m, s) )

print( "task finished !!" )
