# -*- coding: utf-8 -*-

import json
import logging
import os
import re
import sys
import time

from colorama import init, Fore, Back
from pathlib import Path

#======================================================================================================
### 在 windows 10 的 PowerShell 啟用 colorama
#======================================================================================================
init( convert = True )

#======================================================================================================
### 載入文件 & 讀取內容
#======================================================================================================
file = open( './data/test/test4.json', encoding="utf-8" )
loadedContent = json.load( file )

#======================================================================================================
### 相關函數定義
#======================================================================================================
def keyWordsSearch( queryContent, queryText ):
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
		renderedText = Fore.RESET + Back.RESET + queryContent

	return renderedText + '\r\n'

#======================================================================================================
### 處理內容相關資訊取得
#======================================================================================================
print( '\r' )
print( '【 檔案中的 tweet 數 】 ==> ' + str( len( loadedContent ) ) )
print( '\r\n' )

i = 1
queryText = 'COVID'

for jsonSet in loadedContent:
	print( Fore.RESET + Back.RESET + '第 ' + str( i ) + ' 則 :' + '\n' )
	print( 'username ==> ' + jsonSet['username'] + '\n' )
	print( 'tweet_text ==> ' + keyWordsSearch( jsonSet['tweet_text'], queryText ) )
	print( Fore.RESET + Back.RESET + 'total text count ==> ' + str( len( jsonSet['tweet_text'] ) ) + '\n' )

	if jsonSet['hashtags'] == '':
		print( 'hashtags ==> N / A' + '\n' )
	else:
		print( 'hashtags ==> ' + keyWordsSearch( jsonSet['hashtags'], queryText ) )

	print( Fore.RESET + Back.RESET + '--------------------------------------------------------------------------------------------------------------' )
	print( '\r' )

	i = i + 1

sys.exit()