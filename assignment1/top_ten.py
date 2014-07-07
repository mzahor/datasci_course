#!/usr/bin/python
from __future__ import division
from __future__ import print_function

import sys
import json
import re
import operator
import pprint

from itertools import groupby
from collections import Counter

pp = pprint.PrettyPrinter(indent=4).pprint
   
class Tweet(object):
    def __init__(self, raw_tweet):
        self.hashtags = raw_tweet['entities']['hashtags']

    @classmethod
    def parsable(self, raw_tweet):
        return 'entities' in raw_tweet and len(raw_tweet['entities']['hashtags']) > 0

    def __repr__(self):
        return str(self.__dict__)


class Twitter(object):
    def __init__(self, tweet_file):
        self.tweets = self.load_tweets(tweet_file)

    def load_tweets(self, file_name):
        tweets = []
        with open(file_name) as f:
            for line in f:
                tweets.append(json.loads(line))
        return [Tweet(raw_tweet) for raw_tweet in tweets if Tweet.parsable(raw_tweet)]
        

def main():
    tweet_file = sys.argv[1]
    
    twitter = Twitter(tweet_file)

    hashtags = [hashtag[u'text'] for tweet in twitter.tweets for hashtag in tweet.hashtags]

    hashtags_count = Counter(hashtags)
    sorted_hashtags = sorted(hashtags_count.iteritems(), key=operator.itemgetter(1), reverse=True)

    for hashtag in sorted_hashtags[0:10]:
        print (hashtag[0], hashtag[1])
    

if __name__ == '__main__':
    main()
