import os
from collections import defaultdict
from pprint import pprint

FEED_DIR = os.path.abspath(".")
FEED_FILE = os.path.join(FEED_DIR, 'feed.txt')

PARTY_CODE = {
    "C": "Conservative Party",
    "L": "Labour Party",
    "UKIP": "UKIP",
    "LD": "Liberal Democrats",
    "G": "Green Party",
    "Ind": "Independent",
    "SNP": "SNP"
}

RESULTS = defaultdict(dict)


# def display_result(fields):

def parse_feed(file):
    with open(file) as f:
        for line in f.readlines():
            constituency = line[0:line.index(',')]
            fields = line[line.index(',') + 1:].replace(',', '').split()
            fields = [tuple(fields[i:i + 2]) for i in range(0, len(fields), 2)]
            result = {p_code:int(vote) for vote, p_code in fields}
            RESULTS[constituency] = result

def display_result():
    for const, result in RESULTS.items():
        total = sum(result.values())
        print("{}(Total:{})".format(const,total))
        for p_code, vote in result.items():
            print("\t{}: {:.2%}".format(PARTY_CODE[p_code], float(vote)/float(total)))

parse_feed(FEED_FILE)
display_result()