# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import time
import xml.etree.ElementTree as ET

from pathlib import Path

tree = ET.parse( './data/dev/test1.xml' )
root = tree.getroot()

#======================================================================================================
### 計算此 xml 檔中的內容組數
#======================================================================================================
pubmedElement = []

for elem in root.iter( 'PubmedArticle' ):
	pubmedElement.append( elem )

countPubmedArticle = len( pubmedElement )

#======================================================================================================
### 相關函數定義
#======================================================================================================
'''def findCharacterPosition( content, queryText ):
	result = content.find( queryText )

	if result != -1:
		startPosition = result + 1
		print( queryText + ' is start from ' + str( startPosition ) + ' character ~' )
	else:
		print( queryText + ' is not in the content ~' )'''

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
### queryContent[0] ==> articleTitle
### queryContent[1] ==> abstract
### queryContent[2] ==> queryContent
###
#====================================================================================================== 
queryContent = composeQueryContent( pubmedElement[1] )

queryText = 'Pat'
#result = queryContent.find( queryText )

if queryText in queryContent[2]:
	print( queryText + ' is in the content ~' + '\r\n' )
else:
	print( queryText + ' is not in the content ~' + '\r\n' )

#======================================================================================================
### 處理內容相關資訊取得
###
### pmeInfo[0] ==> characterCountAll
### pmeInfo[1] ==> wordCountAll
### pmeInfo[2] ==> allContent
###
#======================================================================================================
pmeInfo = pubmedElementInfo( pubmedElement[1] )
print( pmeInfo[0] )

sys.exit()