# -*- coding: utf-8 -*-
#
# 載入所有 pubmed 資料，並加入 Porter’s algorithm
#

import glob
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import re
import sys

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

#======================================================================================================
### 載入檔案、處理不重覆語詞、計算詞頻
#======================================================================================================
stemmer = PorterStemmer()

dCount = 0
bagOfWords = {}
path = "./data/hw2_data/*.csv"

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
			
			# 包含停用詞與標點符號 :: list
			#filteredText = [word for word in nltk.word_tokenize( text )]

			# 去除標點符號 :: string
			filteredText = re.sub( r'[^a-zA-Z0-9\s]', '', string = text )
			
			# 去除停用詞 :: list
			filteredText = [word for word in nltk.word_tokenize( filteredText ) if word not in stopwords.words( 'english' )]
			
			for word in filteredText:
				
				word = stemmer.stem( word )

				if word not in bagOfWords:
					bagOfWords[word] = 1
				else:
					bagOfWords[word] = bagOfWords[word] + 1

	else:
		break

# 將計數用的詞袋依計數重新排序
sortedBagOfWords = sorted( bagOfWords.items(), key = lambda x:x[1], reverse = True )

# 顯示不重覆的總語詞數
print( len( sortedBagOfWords ) )

# 顯示處理後前 25 名的語詞與其計數
df01 = pd.DataFrame( sortedBagOfWords )
print( df01[:50] )

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

plt.xticks( fontsize = 8 )
plt.xticks( rotation = 270 )

# 避免被圖表元素被蓋住
plt.tight_layout()

plt.plot( word, frequency, lw = 2 )

plt.show()