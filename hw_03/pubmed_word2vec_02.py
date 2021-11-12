# -*- coding: utf-8 -*-
#
# 載入預訓練好的 word2vec
#

import os
import sys
import pandas as pd
import pickle

from gensim.models import word2vec

#======================================================================================================
### 函數定義 :: 詞向量最相近的前 N 筆
#======================================================================================================
def most_similar( w2v_model, words, topn ):
    similar_df = pd.DataFrame()
    for word in words:
        try:
            similar_words = pd.DataFrame( w2v_model.wv.most_similar( word, topn = topn ), columns = [word, 'cos'] )
            similar_df = pd.concat( [similar_df, similar_words], axis = 1 )
        except:
            print( word, "not found in Word2Vec model!" )
    return similar_df   

#======================================================================================================
### 載入模型並執行函數
#======================================================================================================
model = word2vec.Word2Vec.load("./w2v_model/word2vec_dim_200_train_10.model")

print( most_similar( model, ['COVID19', 'coronavirus', 'vaccine' ], 20 ) )

sys.exit()