# -*- coding: utf-8 -*-

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
tree = ET.parse( './data/dev/test1.xml' )
root = tree.getroot()

# 在 windows 10 的 PowerShell 啟用 colorama
init( convert = True )

#======================================================================================================
### 計算此 xml 檔中的內容組數
#======================================================================================================
pubmedElement = []

for elem in root.iter( 'PubmedArticle' ):
	pubmedElement.append( elem )

# 計算載入的 pubmed 檔案中的文章數
countPubmedArticle = len( pubmedElement )

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
		renderedText = 'no matched words !!'

	return renderedText

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
### 對組出的內容作關鍵字搜尋 :: ArticleTitle, Abstract
###
### composedContent[0] ==> articleTitle
### composedContent[1] ==> abstract
### composedContent[2] ==> queryContent
###
#====================================================================================================== 
composedContent = composeQueryContent( pubmedElement[1] )

queryContent = composedContent[2]
queryText = 'SOFA'

queryResult = keyWordsSearch( queryContent, queryText )

print( queryResult )

sys.exit()

#======================================================================================================
### 處理 abstract 相關數字統計
#======================================================================================================
abstractInfo = abstractInfo( pubmedElement[1] )

abstract = abstractInfo[0]
abstractParagraphCount = len( abstract )
abstractSentenceCount = abstractInfo[1]

print( abstractInfo )

#======================================================================================================
### 處理內容相關資訊取得
###
### pmeInfo[0] ==> characterCountAll
### pmeInfo[1] ==> wordCountAll
### pmeInfo[2] ==> allContent
###
#======================================================================================================
pmeInfo = pubmedElementInfo( pubmedElement[1] )
print( pmeInfo )

sys.exit()