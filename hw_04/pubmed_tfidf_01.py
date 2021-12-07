# -*- coding: utf-8 -*-
#
# 載入所有 pubmed abstract 資料，進行 tf-idf 的預處理
#

import glob
import nltk
import pandas as pd
import pickle
import re
import sys
import time

from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

#======================================================================================================
### Basic Settings
#======================================================================================================
# 記錄執行時間_開始
start_time = time.time()

dCount = 0
sentences = []
path = "../hw_02/data/hw2_data/*.csv"

#======================================================================================================
### 載入檔案進行預處理
#======================================================================================================
# 載入要處理的 pubmed 內容 :: 所有檔案
for fileName in glob.glob( path ):
    if dCount < 100:
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
            if text not in sentences:
                # 將分詞後的句子加入到 sentences 變數中
                sentences.append( text )
    else:
        break

# 將 sentences 從 list 轉成 dataframe 再轉成 series，以符合後續計算所需的變數型態
sentencesDF = pd.DataFrame( sentences )
sentencesSeries = sentencesDF.squeeze()

# 計算詞頻
vectorizer = CountVectorizer( stop_words = None, token_pattern = "(?u)\\b\\w+\\b" )  
X = vectorizer.fit_transform( sentencesSeries )
r = pd.DataFrame( X.toarray(), columns = vectorizer.get_feature_names() )
#print( r )
#sys.exit()

# 轉換為 IDF
transformer = TfidfTransformer( smooth_idf = True )
Z = transformer.fit_transform( X )
r = pd.DataFrame( Z.toarray(), columns = vectorizer.get_feature_names(), index=[sentencesSeries] )
#print( r['would'][4] )

# 將結果寫入 csv 檔保存
r.to_csv( './data/tfidf_20211207am_01.csv' )

sys.exit()