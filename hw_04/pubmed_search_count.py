# -*- coding: utf-8 -*-
#
# 進行特定關鍵字作搜尋，以記錄其搜尋結果計數
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
from nltk.tokenize import sent_tokenize

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
    if dCount < 100:
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
print( len( sentences ) )
sys.exit()

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

#======================================================================================================
### 對組出的內容作關鍵字搜尋
#====================================================================================================== 
queryText01 = 'vaccine'

# 對文章內容作搜尋
matchedResult01 = keyWordsSearch( sentences, queryText01 )

queryText02 = 'mRNA'

# 對文章內容作搜尋
matchedResult02 = keyWordsSearch( matchedResult01, queryText02 )

print( len( matchedResult02 ) )

sys.exit()