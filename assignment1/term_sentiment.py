#!/usr/bin/python
from __future__ import division
from __future__ import print_function

import sys
import json
import re
import operator
import pprint

pp = pprint.PrettyPrinter(indent=4).pprint

class Scorer(object):
    def __init__(self, afinn_file):
        self.scores = self.load_scores(afinn_file)

    def __getitem__(self, item):
        return self.get_score(item)

    def load_scores(self, file_name):
        scores = {}
        for line in open(file_name):
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            scores[unicode(term, 'unicode-escape')] = int(score)  # Convert the score to an integer.
        return scores

    def sentence_score(self, sentence):
        score = reduce(operator.add, [self.get_score(word) for word in self.words(sentence)], 0)
        return score

    def words(self, sentence):
        return re.findall(r'\w+', sentence.lower())

    def get_score(self, word):
        return self.scores[word] if word in self.scores else 0
   
class Twitter(object):
    def __init__(self, tweet_file):
        self.tweets = self.load_tweets(tweet_file)

    def load_tweets(self, file_name):
        tweets = []
        with open(file_name) as f:
            for line in f:
                tweets.append(json.loads(line))
        return [tweet['text'] for tweet in tweets if 'text' in tweet]

def main():
    afinn_file = sys.argv[1]
    tweet_file = sys.argv[2]
    
    scorer = Scorer(afinn_file)
    twitter = Twitter(tweet_file)

    words = {}

    for tweet in twitter.tweets:
        tweet_words = set(scorer.words(tweet))
        tweet_score = scorer.sentence_score(tweet)
        for word in tweet_words:
            if word not in words:
                words[word] = {'pos': 1, 'neg': 1}
            if tweet_score > 0:
                words[word]['pos'] += 1
            elif tweet_score < 0:
                words[word]['neg'] += 1

    for word, emo in words.iteritems():
        print(word, emo['pos'] / emo['neg'])

    # print sorted([(word, emo['pos']/emo['neg']) for word, emo in words.iteritems()], key = lambda item: item[1])

if __name__ == '__main__':
    main()
