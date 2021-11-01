# -*- coding: utf-8 -*-
#
# PubMed Parser :: Compare The Content from Two Picked Abstract
#

import re
import sys
import xml.etree.ElementTree as ET

from colorama import init, Fore, Back


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

# 對兩篇文章的內容文字作逐一比對
def contentTextCompare( article01, article02 ):
	compareResult = ''
	sameWordsCount = 0

	# 分為第一篇文章字數較多或第二篇文章字數較多的情況
	if len( article01 ) >= len( article02 ):
		for i in range( len( article01 ) ):
			if i < len( article02 ):
				if article01[i] == article02[i]:
					sameWordsCount = sameWordsCount + 1
					compareResult = compareResult + Fore.WHITE + Back.GREEN + article02[i] + ' '
				else:
					compareResult = compareResult + Fore.WHITE + Back.RED + article02[i] + ' '
			else:
				break
	else:
		for i in range( len( article02 ) ):
			if i < len( article01 ):
				if article01[i] == article02[i]:
					sameWordsCount = sameWordsCount + 1
					compareResult = compareResult + Fore.WHITE + Back.GREEN + article02[i] + ' '
				else:
					compareResult = compareResult + Fore.WHITE + Back.RED + article02[i] + ' '
			else:
				compareResult = compareResult + Fore.RESET + Back.RESET + article02[i] + ' '

	return compareResult, sameWordsCount

#======================================================================================================
### 定義內容來源 01
#======================================================================================================
# 載入文件
tree01 = ET.parse( './data/test/test1.xml' )
root01 = tree01.getroot()

pubmedElement01 = []

for elem01 in root01.iter( 'PubmedArticle' ):
	pubmedElement01.append( elem01 )

# 取得第一篇文章的 Abstract
composedContent01 = composeQueryContent( pubmedElement01[0] )
pbAbstract01 = composedContent01[1]

#======================================================================================================
### 定義內容來源 02
#======================================================================================================
# 載入文件
tree02 = ET.parse( './data/test/test1.xml' )
root02 = tree02.getroot()

pubmedElement02 = []

for elem02 in root02.iter( 'PubmedArticle' ):
	pubmedElement02.append( elem02 )

# 取得第二篇文章的 Abstract
composedContent02 = composeQueryContent( pubmedElement02[0] )
pbAbstract02 = composedContent02[1]

#======================================================================================================
### 組出要作比對的內容
#======================================================================================================
# 對 pbAbstract01 作字詞拆解
wordsInPBAbstract01 = pbAbstract01.split()

# 對 pbAbstract02 作字詞拆解
wordsInPBAbstract02 = pbAbstract02.split()

#======================================================================================================
### 進行內容比對
### compareResult[0] ==> compareResult
### compareResult[1] ==> sameWordsCount
###
#======================================================================================================
compareResult = contentTextCompare( wordsInPBAbstract01, wordsInPBAbstract02 )

#======================================================================================================
### 輸出文章相關摘要資訊與比對結果
#======================================================================================================
# 第一篇文章的內容
print( '\n' )
print( '第一篇文章的內容 ==> ' )
print( pbAbstract01 )
print( '\n' )
print( '第一篇文章字數 ==> ' + str( len( wordsInPBAbstract01 ) ) )
print( '--------------------------------------------------------------------------------------------------------------' )

# 第二篇文章的內容
print( '\n' )
print( '第二篇文章的內容 ==> ' )
print( pbAbstract02 )
print( '\n' )
print( '第二篇文章字數 ==> ' + str( len( wordsInPBAbstract02 ) ) )
print( '--------------------------------------------------------------------------------------------------------------' )

# 逐字比對第二篇文章與第一篇文章內容差異的結果
print( '\n' )
print( '逐字比對第二篇文章與第一篇文章內容差異的結果 ==> ' )
print( compareResult[0] )
print( '\n' )
print( Fore.RESET + Back.RESET + '第二篇文章與第一篇相同的字數 ==> ' + str( compareResult[1] ) + '/' + str( len( wordsInPBAbstract02 ) ) )
print( '\n' )
print( Fore.RESET + Back.RESET + '第二篇文章與第一篇的相似度為 ==> ' + str( round( compareResult[1]/len( wordsInPBAbstract02 ), 8 ) * 100 ) + '%' )
print( '\n\n' )

sys.exit()