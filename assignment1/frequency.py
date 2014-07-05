#!/usr/bin/python
from __future__ import division
from __future__ import print_function

import sys
import json
import re
import operator
import pprint
from collections import Counter

pp = pprint.PrettyPrinter(indent=4).pprint

class Twitter(object):
    def __init__(self, tweet_file):
        self.tweets = self.load_tweets(tweet_file)

    def load_tweets(self, file_name):
        tweets = []
        with open(file_name) as f:
            for line in f:
                tweets.append(json.loads(line))
        return [tweet['text'] for tweet in tweets if 'text' in tweet]

    def all_words(self):
        return [word for tweet in self.tweets for word in self.words(tweet)]

    def words(self, sentence):
        return re.findall(r'\w+', sentence.lower())

def main():
    tweet_file = sys.argv[1]
    
    twitter = Twitter(tweet_file)

    words = twitter.all_words()

    count_all = len(words)

    wcounter = Counter(words)

    for (word, freq) in wcounter.iteritems():
        print(word, freq / count_all)

    # pp(words)


if __name__ == '__main__':
    main()
