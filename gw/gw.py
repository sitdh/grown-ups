# -*- coding: utf-8 -*-

import twitter as tw
import json
import re
import os 
from api import TwitterCredential as tc

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

        for media in meidas:
            if 'photo' == media['type']:
                url += "%s^%s" % (media['id_str'], media['media_url'])

        return url


    def save(self, message):

        self.prepare()

        with open(self.location, 'a') as message_location:
            media_formatted = self.formatted_media(message['media']) if 'media' in message else ''

            message_location.write("%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (message['user']['id_str'], message['id_str'], message['user']['screen_name'], message['text'], media_formatted, message['retweet_count'], message['favorite_count'], message['created_at'], message['timestamp_ms']))

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
        auth = tw.OAuth(tc.OAUTH_TOKEN, 
                tc.OAUTH_TOKEN_SECRET, 
                tc.CONSUMER_KEY, 
                tc.CONSUMER_SECRET)

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
                print("%s: %s " % (tweet['user']['screen_name'], tweet['text']))

if __name__ == "__main__":
    twConn = TwitterConnection()

    fileStore = FileDataStore()
    fileStore.location = 'raw-data.csv'

    search = SearchCollection(twConn.getInstance())
    search.collect('#โตมากับ', fileStore, RemoveRetweetFilter())
