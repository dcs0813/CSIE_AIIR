# -*- coding: utf-8 -*-
#
# 進行特定關鍵字的搜尋處理，並載入預處理好的 tf-idf 作加權計算後作排序顯示
#

import glob
import nltk
import numpy as np
import pandas as pd
import pickle
import re
import sys
import time

from colorama import init, Fore, Back
from gensim.models import word2vec
from nltk.tokenize import sent_tokenize
from pathlib import Path

#======================================================================================================
### Basic Settings
#======================================================================================================
# 記錄執行時間_開始
start_time = time.time()

# 在 windows 10 的 PowerShell 啟用 colorama
init( convert = True )

dCount = 0
sentences = []
path = "../hw_02/data/hw2_data/*.csv"

#======================================================================================================
### 載入檔案進行預處理
#======================================================================================================
# 載入要處理的 pubmed 內容 :: 所有檔案
for fileName in glob.glob( path ):
    if dCount < 2:
        # 處理計數
        #print( dCount )
        dCount = dCount + 1

        # 讀取檔案
        df = pd.read_csv( fileName, encoding='utf8' )

        # 去除掉內容為空的部份
        df = df.dropna()

        # 只取 abstract 的部份
        content = df['abstract']

        for text in content:
            # 將分詞後的句子加入到 sentences 變數中
            sentences.append( text )   
    else:
        break

#======================================================================================================
### 相關函數定義
#======================================================================================================
# 關鍵字搜尋
def keyWordsSearch( queryContent, queryText ):
	matchedResult = []
	for content in queryContent:
		# 對內容作特定字詞搜尋
		result = [i for i in range( len( content ) ) if content.startswith( queryText, i ) ]
		if result != []:
			matchedResult.append( content )

	return matchedResult


def searchResultColoredDisplay( queryContent, queryText ):	
	j = 0
	result = {}

	for qText in queryText:
		result[j] = [i for i in range( len( queryContent ) ) if queryContent.startswith( qText, i ) ]
		j += 1

	print( result )
	print( '\r\n' )
	renderedText = ""
	wordRenderingFirstCount = 0
	textPositionPadding = 0

	for key, value in result.items():
		for i in value:
			#print( i )
			if key == 0:
				matchedKeyWord = Fore.RED + Back.WHITE + queryContent[i:(i+len( queryText[key] ) )] + Fore.RESET + Back.RESET
				#queryContent = queryContent.replace( queryContent[i:(i+len( queryText[key] ) )], matchedKeyWord )
				print( len( queryText[key] ) )
				print( len( matchedKeyWord ) )
				print( '\r' )

			elif key == 1:
				matchedKeyWord = Fore.GREEN + Back.WHITE + queryContent[i:(i+len( queryText[key] ) )] + Fore.RESET + Back.RESET
				#queryContent = queryContent.replace( queryContent[i:(i+len( queryText[key] ) )], matchedKeyWord )
				print( len( queryText[key] ) )
				print( len( matchedKeyWord ) )
				print( '\r' )
				#sys.exit()
				
			'''else:
				break'''
	#print( queryContent )
	sys.exit()
	
	# 未完成 …… 尚未採用, 2021/12/7
	return renderedText + '\r\n'

def keyWordsSearch002( queryContent, queryText ):
	# 對內容作特定字詞搜尋
	result = [i for i in range( len( queryContent ) ) if queryContent.startswith( queryText, i ) ]

	if len( result ) == 1:
		renderedText = ""
		contentBeforeKeyword = Fore.WHITE + Back.BLUE + queryContent[:(result[0])]
		keywordMatched = Fore.RED + Back.WHITE + queryContent[result[0]:(result[0]+len(queryText))]
		contentAfterKeyword = Fore.WHITE + Back.BLUE + queryContent[(result[0]+len(queryText)):]
		
		renderedText = renderedText + contentBeforeKeyword + keywordMatched + contentAfterKeyword

	elif len( result ) > 1:
		renderedText = ""
		for i in range( len( result ) ):
			if i == 0:
				contentBeforeKeyword = Fore.WHITE + Back.BLUE + queryContent[:(result[i])]
				keywordMatched = Fore.RED + Back.WHITE + queryContent[result[i]:(result[i]+len(queryText))]
				
				renderedText = renderedText + contentBeforeKeyword + keywordMatched

			elif i == ( len( result ) - 1 ):
				contentBeforeKeyword = Fore.WHITE + Back.BLUE + queryContent[(result[i-1]+len(queryText)):(result[i])]
				keywordMatched = Fore.RED + Back.WHITE + queryContent[result[i]:(result[i]+len(queryText))]
				contentAfterKeyword = Fore.WHITE + Back.BLUE + queryContent[(result[i]+len(queryText)):]
				
				renderedText = renderedText + contentBeforeKeyword + keywordMatched + contentAfterKeyword

			else:
				contentBeforeKeyword = Fore.WHITE + Back.BLUE + queryContent[(result[i-1]+len(queryText)):(result[i])]
				keywordMatched = Fore.RED + Back.WHITE + queryContent[result[i]:(result[i]+len(queryText))]
				
				renderedText = renderedText + contentBeforeKeyword + keywordMatched

	else:
		renderedText = Fore.WHITE + Back.RED + 'no matched words !!' + '\n' + Fore.RESET + Back.RESET + queryContent

	return renderedText + Fore.RESET + Back.RESET + '\r'


#======================================================================================================
### 對組出的內容作關鍵字搜尋
#====================================================================================================== 
queryText01 = 'COVID-19'

# 對文章內容作搜尋
matchedResult01 = keyWordsSearch( sentences, queryText01 )

queryText02 = 'SARS'

# 對文章內容作搜尋
matchedResult02 = keyWordsSearch( matchedResult01, queryText02 )

#======================================================================================================
### 載入預訓練好的 tf-idf
#======================================================================================================
# 讀取檔案
dfTDIDF = pd.read_csv( './data/tfidf_20211205am_01.csv', encoding='utf8' )

# 將載入的 csv 中主要文字內容的欄位重新命名
dfTDIDF.rename( columns={'Unnamed: 0':'content'}, inplace=True )

# 預定義變數
qResultIndex = []
tfidfScore = {}

# 將搜尋結果和載入的 tf-idf 文件作比對及積分計算
for qResult in matchedResult02:
	if qResult in dfTDIDF.content.values:

		# 取得與搜尋結果相符的 index
		rowIndex = dfTDIDF.index[dfTDIDF['content'] == qResult ].tolist()
		#qResultIndex.append( rowIndex[0] )

		# 取得該 index 對應 row 的 tf-idf 分數加總
		countResult = dfTDIDF.iloc[ rowIndex ].sum( axis = 1 )
		score = countResult.values[0]
		
		# 將 index 和 score 組成 dict
		tfidfScore[rowIndex[0]] = score

# 將結果依積分排序
sortedTfidfScore = sorted( tfidfScore.items(), key=lambda x: x[1], reverse = True )

#======================================================================================================
### 輸出依積分排序後的搜尋內容
#======================================================================================================
i = 1

print( '\r\n' )
print( '【 搜尋關鍵字 】 :: ' + queryText01 + ', ' + queryText02 )
print( '\r\n' )

for text in sortedTfidfScore:
	text = list( text )
	textIndex = text[0]
	textScore = text[1]
	
	print( '\r' )
	print( '【 第 ' + str( i ) + '篇 】' )
	print( '\r' )
	print( 'Original Index in dfTDIDF ==> ' + str( textIndex ) )
	print( '\r' )
	print( 'Score ==> ' + str( textScore ) )
	print( '\r' )

	queryRender01 = keyWordsSearch002( dfTDIDF['content'][textIndex], queryText01 )
	queryRender02 = keyWordsSearch002( queryRender01, queryText02 )
	print( queryRender02 )

	print( '\r' )
	print( '=====================================================================================================================================' )
	#sys.exit()
	i = i + 1

sys.exit()