# -*- coding: utf-8 -*-
#
# 載入預訓練好的 word2vec 進行降維 & 資料視覺化
#

import gensim
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import pickle
import sklearn

from gensim.models import word2vec
from sklearn.manifold import TSNE

#======================================================================================================
### 函數定義 :: 詞向量最相近的前 N 筆
#======================================================================================================
def get_similar_words( w2v_model, words, topN ):
    similar_words = []   
    for word in words:
        result = w2v_model.wv.most_similar( word, topn = topN )
        for i in range( len( result ) ):
            similar_words.append( result[i][0] )
            #print( result[i][0]  )
        
    return similar_words  

#======================================================================================================
### 載入模型
#======================================================================================================
model = word2vec.Word2Vec.load("./w2v_model/word2vec_dim_200_train_10.model")

# 取得模型中所有訓練的字詞
#words = list(model.wv.index_to_key)
#vocab = list(model.wv.key_to_index)
#print( len( words ) )
#sys.exit()

# 取得特定字詞的 index
#print( model.wv.key_to_index['COVID19'])

# 取得模型中所有訓練的詞向量
#word_vectors = model.wv
#print( word_vectors['vaccine'] )

#print( most_similar( model, ['COVID19' ], 6 ) )
#sys.exit()

#======================================================================================================
### 作資料定義與降維
#======================================================================================================
# 預定義相關變數
topN = 20
tsne = TSNE(n_components=2)

# 定義要作檢視與比對的語詞
vocab = get_similar_words( model, ['COVID19'], topN )
X = model.wv[vocab]
X_tsne = tsne.fit_transform(X)
df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

# 定義要作檢視與比對的語詞
'''vocab1 = get_similar_words( model, ['coronavirus'], topN )
X1 = model.wv[vocab1]
X_tsne1 = tsne.fit_transform(X1)
df1 = pd.DataFrame(X_tsne1, index=vocab1, columns=['x', 'y'])

# 定義要作檢視與比對的語詞
vocab2 = get_similar_words( model, ['vaccine'], topN )
X2 = model.wv[vocab2]
X_tsne2 = tsne.fit_transform(X2)
df2 = pd.DataFrame(X_tsne2, index=vocab2, columns=['x', 'y'])'''

#======================================================================================================
### 進行資料視覺化
#======================================================================================================
fig = plt.figure()
fig.set_size_inches( 12, 8 )
ax = fig.add_subplot(1, 1, 1)

ax.scatter(df['x'], df['y'])
#ax.scatter(df1['x'], df1['y'])
#ax.scatter(df2['x'], df2['y'])

for word, pos in df.iterrows():
    ax.annotate(word, pos)

'''for word, pos in df1.iterrows():
    ax.annotate(word, pos)

for word, pos in df2.iterrows():
    ax.annotate(word, pos)'''

plt.show()
sys.exit()
