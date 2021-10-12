# -*- coding: utf-8 -*-
#
# PubMed Parser :: All Content
#

import logging
import os
import re
import sys
import time
import xml.etree.ElementTree as ET

from colorama import init, Fore, Back
from pathlib import Path

#======================================================================================================
### 載入文件
#======================================================================================================
tree = ET.parse( './data/dev/test3.xml' )
root = tree.getroot()

# 在 windows 10 的 PowerShell 啟用 colorama
init( convert = True )

#======================================================================================================
### 相關函數定義
#======================================================================================================
def composeQueryContent( pubmedElement ):
	articleTitle = ''
	abstract = ''
	queryContent = ''
	
	# 取得 ArticleTitle 的內容文字
	for node in pubmedElement.iter('ArticleTitle'):
		articleTitle = node.text
		queryContent = queryContent + node.text

	# 取得 Abstract 的內容文字
	for node in pubmedElement.iter('Abstract'):
		for elem in node.iter('AbstractText'):
			abstract = abstract + elem.text
			queryContent = queryContent + elem.text

	return articleTitle, abstract, queryContent

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
		renderedText = Fore.WHITE + Back.RED + 'no matched words !!' + '\n' + Fore.RESET + Back.RESET + queryContent

	return renderedText + '\r\n'

def abstractInfo( pubmedElement ):
	abstract = []
	setenceCount = 0

	# 取得 Abstract 的內容文字
	for node in pubmedElement.iter('Abstract'):
		for elem in node.iter('AbstractText'):
			abstract.append( elem.text )
			setenceCount = setenceCount + len( list( filter( None,  re.split( r'[.!?]+', elem.text ) ) ) )
	
	return abstract, setenceCount

def pubmedElementInfo( pubmedElement ):
	characterCountAll = 0
	wordCountAll = 0
	allContent = []

	# 取得全部標籤的內容文字
	for node in pubmedElement.iter():
		
		origin = node.text

		# 因為有的內容為換行字元加空白，所以要先將其清除
		processed = origin.strip()

		# 如果清除完只剩空字串，則將其捨棄
		if processed != '':
			characterCount = len( processed )
			characterCountAll = characterCountAll + characterCount

			wordCount = len( processed.split() )
			wordCountAll = wordCountAll + wordCount
			
			allContent.append( processed )
	
	return characterCountAll, wordCountAll, allContent

#======================================================================================================
### 輸出文章相關摘要資訊
#======================================================================================================
pubmedElement = []

for elem in root.iter( 'PubmedArticle' ):
	pubmedElement.append( elem )

# 計算載入的 pubmed 檔案中的文章數
countPubmedArticle = len( pubmedElement )

# 輸出 :: 檔案中的文章數
print( '\n' )
print( '【 檔案中的文章數 】 ==> ' + str( countPubmedArticle ) + '\r\n' )

# 定義變數
i = 1
queryText = 'of '

# 進行內容的遞迴處理
for pmElement in pubmedElement:
	
	# 處理內容相關資訊取得
	pmeInfo = pubmedElementInfo( pmElement )

	# 處理 abstract 相關數字統計
	abstrInfo = abstractInfo( pmElement )

	abstract = abstrInfo[0]
	abstractParagraphCount = len( abstract )
	abstractSentenceCount = abstrInfo[1]

	# 對組出的內容作關鍵字搜尋 :: ArticleTitle, Abstract
	composedContent = composeQueryContent( pmElement )

	# 對文章標題作搜尋
	titleContent = composedContent[0]
	titleQueryResult = keyWordsSearch( titleContent, queryText )

	# 對文章內容作搜尋
	abstractContent = composedContent[1]
	abstractQueryResult = keyWordsSearch( abstractContent, queryText ) 
	
	# 輸出 :: 內容相關資訊
	print( '\n' )
	print( Fore.WHITE + Back.RESET + '=== 第 ' + str( i ) + ' 則 ===' + '\n' )
	print( Fore.RESET + Back.RESET + '文章總字元數 ==> ' + str( pmeInfo[0] ) )
	print( '文章總字數 ==> ' + str( pmeInfo[1] ) )
	print( '--------------------------------------------------------------------------------------------------------------' )

	# 輸出 :: abstract 相關資訊
	print( 'abstract 句子數 ==> ' + str( abstractSentenceCount ) )
	print( 'abstract 段落數 ==> ' + str( abstractParagraphCount ) )
	print( '--------------------------------------------------------------------------------------------------------------' )

	# 輸出 :: keywords search 相關資訊
	print( 'ArticleTitle / Abstract 關鍵字搜尋 ==> \"' + queryText + '\"' )
	print( '\n' )
	print( titleQueryResult )
	print( abstractQueryResult )

	i = i + 1

sys.exit()