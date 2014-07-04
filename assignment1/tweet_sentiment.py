import sys
import json
import pprint

def main():
    pp = pprint.PrettyPrinter(indent=4).pprint

    sent_file = open(sys.argv[1])
    tweet_file = sys.argv[2]

    afinnfile = open("AFINN-111.txt")
    scores = {} # initialize an empty dictionary

    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[unicode(term, 'unicode-escape')] = int(score)  # Convert the score to an integer.

    tweets = []
    with open(tweet_file) as f:
        for line in f:
            tweets.append(json.loads(line))
    
    for tweet in tweets:
        if "text" in tweet:
            pp(tweet["text"]) 
    
    pp(scores[u'fuck'])

if __name__ == '__main__':
    main()
