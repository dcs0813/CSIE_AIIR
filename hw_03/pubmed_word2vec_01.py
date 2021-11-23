# -*- coding: utf-8 -*-
#
# 載入所有 pubmed abstract 資料，進行 word2vec 訓練
#

import glob
import nltk
import pandas as pd
import pickle
import re
import sys
import time

from gensim.models import word2vec
from nltk.tokenize import sent_tokenize

#======================================================================================================
### Basic Settings
#======================================================================================================
# 記錄執行時間_開始
start_time = time.time()

dCount = 0
sentences = []
path = "../hw_02/data/hw2_data/*.csv"

#======================================================================================================
### 載入檔案、對要訓練的內容作預處理
#======================================================================================================
# 載入要處理的 pubmed 內容 :: 所有檔案
for fileName in glob.glob( path ):
    if dCount < 1000:
        # 處理計數
        print( dCount )
        dCount = dCount + 1

        # 讀取檔案
        df = pd.read_csv( fileName, encoding='utf8' )

        # 去除掉內容為空的部份
        df = df.dropna()

        # 只取 abstract 的部份
        content = df['abstract']
        
        for text in content:

            for st in sent_tokenize( text ):

                # 去除標點符號 :: string
                stText = re.sub( r'[^a-zA-Z0-9\s]', '', string = st )
                
                # 分詞 :: list
                filteredText = [word for word in nltk.word_tokenize( stText )]

                # 將分詞後的句子加入到 sentences 變數中
                sentences.append( filteredText )

    else:
        break

#======================================================================================================
### 使用 Word2Vec 訓練詞向量
#======================================================================================================
"""
min_count： 詞頻少於 min_count 之詞彙不會參與訓練
vector_size： 轉成向量的維度
workers： 訓練的並行數量
epochs： 訓練的迭代次數
window： 周圍詞彙要看多少範圍
sg： Word2Vec 有兩種算法, sg=0 採用 cbow，sg=1 採用 skip-gram
seed： 亂數種子
batch_words：每次給予多少詞彙量訓練
"""
model = word2vec.Word2Vec(
    sentences,
    min_count = 3,
    vector_size = 200,
    workers = 3,
    epochs = 10,
    window = 3,
    sg = 1,
    seed = 666,
    batch_words = 10000
)

# 儲存訓練好的模型
model.save("./w2v_model/word2vec_skipgram_dim_200_train_10.model")

#======================================================================================================
### 記錄執行時間 :: 結束
#======================================================================================================
end_time = time.time()
seconds = end_time - start_time

# 將執行時間轉換成「 時 : 分 : 秒 」的格式
m, s = divmod( seconds, 60 )
h, m = divmod( m, 60 )

print( '執行時間 :: ', "%d : %02d : %02d" % (h, m, s) )

print( "word2vec model saved !!" )