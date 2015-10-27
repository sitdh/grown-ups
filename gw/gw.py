# -*- coding: utf-8 -*-

import twitter as tw
import json
import re
import os 
from api import TwitterCredential as tc

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

"""
################################
Data Collection
"""
class DataStore:
    def __init__(self):
        pass

    def save(self, message):
        """Save message"""

class FileDataStore(DataStore):

    location = ''

    def __init__(self):
        pass

    def prepare(self):
        if '' == self.location:
            self.location = 'ex-raw-data.csv'

        if os.path.isfile(self.location):
            with open(self.location, 'w') as tweets:
                tweets.write("uid|mid|screen_name|text|medias|retweet_count|fav_count|tweet_date|timestamp_ms\n")
                tweets.close()

    def formatted_media(self, medias):
        url = ""

        for media in medias:
            if 'photo' == media['type']:
                url += "%s^%s" % (media['id_str'], media['media_url'])

        return url


    def save(self, message):

        self.prepare()

        media_formatted = self.formatted_media(message['entities']['media']) if 'media' in message['entities'] else ''
        m = message['user']['id_str'] + "|" + message['id_str'] + "|" + message['user']['screen_name'] + "|" + message['text'] + "|" + media_formatted + "|" + str(message['retweet_count']) + "|" + str(message['favorite_count']) + "|" + str(message['created_at']) + "|" + str(message['timestamp_ms'])

        with open(self.location, 'a') as message_location:
            self.prepare()

            message_location.write(m)
            message_location.flush()
            message_location.close()

class RemoveRetweetFilter:

    __regex = None 
    
    def __init__(self):
        self.__regex = re.compile(r"rt", re.IGNORECASE) 

    def filter(self, message):
        return (0 == len(self.__regex.findall(message)))

"""
################################
Twitter Object
"""
class TwitterConnection:
    def __init__(self):
        pass

    def getInstance(self):
        credential = tc()
        cr = credential.credential()
        auth = tw.OAuth(cr['oauth_token'], 
                cr['oauth_token_secret'], 
                cr['consumer_key'], 
                cr['consumer_secret'])

        return auth

"""
################################
Search Collection
"""
class SearchCollection:

    __connector = None

    def __init__(self, connector):
        self.__connector = tw.TwitterStream(auth=connector)

    def collect(self, q, datastore, twfilter):
        if not isinstance(datastore, DataStore):
            print 'Could not store message in this datastore'
            datastore = DataStore()

        tweets = self.__connector.statuses.filter(track=q)

        for tweet in tweets:
            if twfilter.filter(tweet['text']):
                datastore.save(tweet) 

if __name__ == "__main__":
    twConn = TwitterConnection()

    fileStore = FileDataStore()
    fileStore.location = 'raw-data.csv'

    search = SearchCollection(twConn.getInstance())
    search.collect('#โตมากับ', fileStore, RemoveRetweetFilter())
