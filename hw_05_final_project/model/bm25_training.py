# -*- coding: utf-8 -*-
#
# AIIR Final Project :: 載入預訓練好的 word2vec 作相關字詞搜尋
#

import os
import sys
import pandas as pd
import pickle
import time

from rank_bm25 import BM25Okapi

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
### 執行
#======================================================================================================
# 記錄執行時間_開始
start_time = time.time()

# 讀取 & 建立搜尋基底
queryContent = getQueryContent()

# 將搜尋基底作簡單的分詞
tokenizedQueryContent = [content.split(" ") for content in queryContent]

# BM25
bm25 = BM25Okapi( tokenizedQueryContent )

#To save bm25 object
with open('./bm25_model/bm25_document_200', 'wb') as bm25_result_file:
    pickle.dump( bm25, bm25_result_file )

#======================================================================================================
### 計算執行時間
#======================================================================================================
end_time = time.time()
seconds = end_time - start_time

# 將執行時間轉換成「 時 : 分 : 秒 」的格式
m, s = divmod( seconds, 60 )
h, m = divmod( m, 60 )

print( '執行時間 :: ', "%d : %02d : %02d" % (h, m, s) )

print( "bm25 model saved !!" )
