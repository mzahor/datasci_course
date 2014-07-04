import sys
import json
import re
import operator
import pprint

scores = {} # initialize an empty dictionary
pp = pprint.PrettyPrinter(indent=4).pprint

def main():
    afinnfile = open(sys.argv[1])
    tweet_file = sys.argv[2]
    
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[unicode(term, 'unicode-escape')] = int(score)  # Convert the score to an integer.

    tweets = []
    with open(tweet_file) as f:
        for line in f:
            tweets.append(json.loads(line))
    
    results = []
    for tweet in tweets:
        if "text" in tweet:
            # pp(tweet['text'])
            score = get_score_for_tweet(tweet['text'])
            pp(score)
            results.append((tweet['text'], score,))

    # the most awful tweets last
    # pp(sorted(results, key=lambda x:x[1], reverse=True))

def get_score_for_tweet(tweet):
    words = re.findall(r'\w+', tweet.lower())
    score = reduce(operator.add, [get_score(word) for word in words], 0)
    return score

def get_score(word):
    return scores[word] if word in scores else 0

if __name__ == '__main__':
    main()
