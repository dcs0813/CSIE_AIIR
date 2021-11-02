# -*- coding: utf-8 -*-
#
# 載入所有 pubmed 資料，並透過 edit distance 作特定關鍵字的比對搜尋
#

import glob
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import re
import sys

from colorama import init, Fore, Back
from nltk.metrics import edit_distance

# 在 windows 10 的 PowerShell 啟用 colorama
init( convert = True )

#======================================================================================================
### 預定義相關變數
#======================================================================================================
articleNum = 3
inputText = 'COVID-19'
eDistance = 2
dCount = 0
bagOfWords = {}
path = "./data/hw2_data/*.csv"

# 在 terminal 介面顯示搜尋的字詞
print( '\r' )
print( 'Search Keyword ==> ' + inputText )
print( '\r' )
print( 'Edit Distance ==> ' + str( eDistance ) )
print( '--------------------------------------------------------------------------------------------------------------' )
print( '\r' )

#======================================================================================================
### 載入檔案、透過 edit distance 作字詞搜尋
#======================================================================================================
# 載入要處理的 pubmed 內容 :: 所有檔案
for fileName in glob.glob( path ):
	
	# 定義要取出多少篇內容
	if dCount < articleNum:
		
		# 處理計數
		dCount = dCount + 1

		# 讀取檔案
		df = pd.read_csv( fileName, encoding='utf8' )

		# 去除掉內容為空的部份
		df = df.dropna()

		# 只取 abstract 的部份
		content = df['abstract']

		for text in content:
			renderedText = ""

			# 使用 nltk 處理分詞
			filteredText = [word for word in nltk.word_tokenize( text )]
			
			# 對內容中的文字與要搜尋的關鍵字用 edit distance 作逐字比對
			for word in filteredText:

				# 定義要比對的 edit distance 數值
				if edit_distance( inputText, word ) <= eDistance:
					keywordMatched = Fore.RED + Back.WHITE + word
					renderedText = renderedText + keywordMatched + Fore.RESET + Back.RESET + ' '
				else:
					renderedText = renderedText + Fore.RESET + Back.RESET + word + ' '
		
		print( renderedText )
		print( '--------------------------------------------------------------------------------------------------------------' )
		print( '\r' )				

	else:
		break

sys.exit()