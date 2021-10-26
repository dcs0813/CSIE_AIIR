# -*- coding: utf-8 -*-
#
# 參考網址 ==> https://towardsdatascience.com/tweepy-for-beginners-24baf21f2c25
#
#

import csv
import datetime
import json
import pandas as pd
import random
import re
import sys
import time
import tweepy

from decouple import config

#======================================================================================================
### 類別與函式定義 :: TweetMiner
#======================================================================================================
class TweetMiner():

    result_limit = 500    
    data = []
    api = False
    
    twitter_keys = {
        'consumer_key': config('consumer_key'),
        'consumer_secret': config('consumer_secret'),
        'access_token_key': config('access_token_key'),
        'access_token_secret': config('access_token_secret')
    }
    
    def __init__( self, keys_dict = twitter_keys, api = api, result_limit = 500 ):
        
        self.twitter_keys = keys_dict
        
        auth = tweepy.OAuthHandler( keys_dict['consumer_key'], keys_dict['consumer_secret'] )
        auth.set_access_token( keys_dict['access_token_key'], keys_dict['access_token_secret'] )
        
        self.api = tweepy.API( auth )
        self.twitter_keys = keys_dict
        self.result_limit = result_limit

    def mine_user_tweets( self, user = "CNN", mine_rewteets = False, max_pages = 100 ):

        data = []
        last_tweet_id = False
        page = 1
        
        while page <= max_pages:
            if last_tweet_id:
                statuses = self.api.user_timeline( screen_name = user,
                                                   count = self.result_limit,
                                                   max_id = last_tweet_id - 1,
                                                   tweet_mode = 'extended',
                                                   include_rts = True )        
            else:
                statuses = self.api.user_timeline( screen_name = user,
                                                   count = self.result_limit,
                                                   tweet_mode = 'extended',
                                                   include_rts = True )
                
            for item in statuses:
                mined = {
                    'tweet_id': item.id,
                    'name': item.user.name,
                    'text': item.full_text,
                    'created_at': item.created_at,
                    'favourite_count': item.favorite_count,
                    'hashtags': item.entities['hashtags']
                }
                
                last_tweet_id = item.id
                data.append( mined )

            print( 'page ==> ' + str( page ) )

            time.sleep( random.randint( 1, 3 ) )
                
            page += 1
            
        return data 

#======================================================================================================
### 執行 API 相關函式
#======================================================================================================
miner = TweetMiner( result_limit = 1 )
mined_tweets = miner.mine_user_tweets()

#print( mined_tweets[0]['text'] )

#======================================================================================================
### 將請求結果寫入 CSV 檔保存
#======================================================================================================
file = open( './data/20211026_pm_01.csv', 'w', encoding = "utf-8", newline = '' )
csvCursor = csv.writer( file )

csvCursor.writerow( [ 'tweet_id', 'name', 'text', 'created_at', 'favourite_count', 'hashtags' ] )

for content in mined_tweets:
    csvCursor.writerow( [ content['tweet_id'], content['name'], content['text'], content['created_at'], content['favourite_count'], content['hashtags'] ] )

sys.exit()