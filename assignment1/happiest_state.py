#!/usr/bin/python
from __future__ import division
from __future__ import print_function

import sys
import json
import re
import operator
import pprint

from itertools import groupby

pp = pprint.PrettyPrinter(indent=4).pprint

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

states_inv = dict ( (state, code) for code, state in states.items() )

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

   
class Tweet(object):
    def __init__(self, raw_tweet):
        self.country, self.state, self.text = self.parse(raw_tweet)

    @classmethod
    def parsable(self, raw_tweet):
        return  'place' in raw_tweet and raw_tweet['place'] and \
                'country_code' in raw_tweet['place'] and \
                'full_name' in raw_tweet['place'] and raw_tweet['place']['full_name'] != None and \
                self.get_state(raw_tweet['place']['full_name']) != None and \
                'text' in raw_tweet

    @classmethod
    def get_state(self, full_name):
        addr = full_name.split(', ')
        if len(addr) != 2:
            return None

        # state can be ['Indiana', 'USA']
        if addr[1] == 'USA' and addr[0] in states_inv:
            return states_inv[addr[0]]
        elif addr[1] in states:
            return addr[1]
        else:
            return None

    def parse(self, raw_tweet):
        country = raw_tweet['place']['country_code']
        state = self.get_state(raw_tweet['place']['full_name'])
        text = raw_tweet['text']
        return country, state, text

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
    afinn_file = sys.argv[1]
    tweet_file = sys.argv[2]
    
    scorer = Scorer(afinn_file)
    twitter = Twitter(tweet_file)

    state_key = lambda x: x.state

    tweets_by_state = groupby(sorted(twitter.tweets, key=state_key), state_key)

    def score_tweets(tweets):
        return reduce(operator.add, [scorer.sentence_score(tweet.text) for tweet in list(tweets)], 0)

    state_happiness = sorted([(state, score_tweets(tweets)) for state, tweets in tweets_by_state], key=operator.itemgetter(1), reverse=True)

    print(state_happiness[0][0])

if __name__ == '__main__':
    main()
