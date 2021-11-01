# -*- coding: utf-8 -*-
#
# 載入單一筆 pubmed 資料
#

import csv
import datetime
import glob
import json
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import random
import re
import sys
import time
import tweepy

from decouple import config
from nltk.corpus import stopwords

'''words = stopwords.words('english')
print( words )
sys.exit()'''

#======================================================================================================
### 載入檔案、處理不重覆語詞、計算詞頻
#======================================================================================================
# 載入要處理的 pubmed 內容 :: 單一檔案
df = pd.read_csv( './data/hw2_data/1.csv', encoding='utf8' )

# 去除掉內容為空的部份
df = df.dropna()

# 只取 abstract 的部份
content = df['abstract']

bagOfWords = {}

for text in content:
	result = nltk.word_tokenize( text )
	for word in result:
		if word not in bagOfWords:
			bagOfWords[word] = 1
		else:
			bagOfWords[word] = bagOfWords[word] + 1

# 將計數用的詞袋依計數重新排序
sortedBagOfWords = sorted( bagOfWords.items(), key = lambda x:x[1], reverse = True )

print( len( sortedBagOfWords ) )

#======================================================================================================
### 預定義相關變數
#======================================================================================================
word = list()
frequency = list()

#======================================================================================================
### 將 sortedBagOfWords 重組成要餵 matplotlib 的格式
#======================================================================================================
i = 0

for data in sortedBagOfWords:
	if i < 100:
		data = list( data )
		d101 = str( data ).split()
		
		# 取得 word
		d102 = d101[0].split( '[' )
		d103 = d102[1].split( ', ' )
		d104 = d103[0].split( ',' )
		word.append( d104[0] )
		
		# 取得數值
		d105 = d101[1].split( ']' )
		frequency.append( float( d105[0] ) )

		i = i + 1

	else:
		break

#======================================================================================================
### 設定 & 執行 matplotlib
#======================================================================================================
figure, ax = plt.subplots()

# 設定圖片顯示尺寸。
# Matplotlib 使用點 point 而非 pixel 為圖的尺寸測量單位，適合用於印刷出版。1 point = 1 / 72 英吋，但可以調整
figure.set_size_inches( 12, 8 )

# 顯示格線
ax.grid( True )

#plt.invert_yaxis()

# 設定標題與軸標籤
plt.xlabel( "word" )
plt.ylabel( "times" )

# 避免被圖表元素被蓋住
plt.tight_layout()

plt.plot( word, frequency, lw = 2 )

plt.show()