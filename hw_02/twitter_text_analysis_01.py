# -*- coding: utf-8 -*-

import csv
import datetime
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


# 載入要處理的 twitter 內容
df = pd.read_csv( './data/twitter_data/20211029_pm_01.csv', encoding='utf8' )
content = df['text']

bagOfWords = {}

for text in content:
	result = nltk.word_tokenize( text )
	for word in result:
		if word not in bagOfWords:
			bagOfWords[word] = 1
		else:
			bagOfWords[word] = bagOfWords[word] + 1

sortedBagOfWords = sorted( bagOfWords.items(), key = lambda x:x[1], reverse = True )

#======================================================================================================
### 預定義相關變數
#======================================================================================================
word = list()
frequency = list()

#======================================================================================================
### 將 sortedBagOfWords 重組成要餵 matplotlib 的格式
#======================================================================================================
for data in sortedBagOfWords:
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