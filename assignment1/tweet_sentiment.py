#!/usr/bin/python
import sys
import json
import re
import operator
import pprint

pp = pprint.PrettyPrinter(indent=4).pprint

def load_scores(file_name):
    scores = {}
    for line in open(file_name):
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[unicode(term, 'unicode-escape')] = int(score)  # Convert the score to an integer.
    return scores

def load_tweets(file_name):
    tweets = []
    with open(file_name) as f:
        for line in f:
            tweets.append(json.loads(line))
    return tweets

def get_score_for_tweet(tweet, scores):
    words = re.findall(r'\w+', tweet.lower())
    score = reduce(operator.add, [get_score(word, scores) for word in words], 0)
    return score

def get_score(word, scores):
    return scores[word] if word in scores else 0

def main():
    afinnfile = sys.argv[1]
    tweet_file = sys.argv[2]
    
    scores = load_scores(afinnfile)
    tweets = load_tweets(tweet_file)

    results = []
    for tweet in tweets:
        if "text" in tweet:
            # pp(tweet['text'])
            score = get_score_for_tweet(tweet['text'], scores)
            pp(score)
            results.append((tweet['text'], score,))

    # the most awful tweets last
    # pp(sorted(results, key=lambda x:x[1], reverse=True))


if __name__ == '__main__':
    main()
