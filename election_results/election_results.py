import os
from collections import defaultdict
from pprint import pprint
import json

FEED_DIR = os.path.abspath(".")
FEED_FILE = os.path.join(FEED_DIR, 'feed.txt')
FEED_ERR = os.path.join(FEED_DIR, 'feed_err.txt')
OVERRIDE_FILE= os.path.join(FEED_DIR, 'override.txt')

PARTY_CODE = {
    "C": "Conservative Party",
    "L": "Labour Party",
    "UKIP": "UKIP",
    "LD": "Liberal Democrats",
    "G": "Green Party",
    "Ind": "Independent",
    "SNP": "SNP"
}

RESULTS = defaultdict(lambda: {})

ERRORS = []


# def display_result(fields):

def report_error(line_no, line, issue):
    err = "Line No: {}\nEntry: {}\nIssue: {}\n{}".format(line_no + 1, line.strip(), issue, "-" * 80)
    ERRORS.append(err)


def save_error_log():
    with open(FEED_ERR, 'w+') as ef:
        ef.write("\n".join(ERRORS))


def valid_entry(line, i):
    if line.startswith('#') or line is None:
        report_error(i, line, "Comment or Empty Line")
        return False
    if ',' not in line:
        report_error(i, line, "Expected delimeter ',' not found in the line")
        return False
    return True


def extract_const(line, i):
    if not valid_entry(line, i):
        return False
    constituency = line[0:line.index(',')]
    if constituency.isnumeric():
        report_error(i, line, "Constituency name  missing or invalid value - {}".format(constituency))
        return False
    return constituency


def extract_vote_info(line, i):
    fields = line[line.index(',') + 1:].replace(',', '').split()
    if len(fields) % 2:
        report_error(i, line, "Either Party Code or Vote info missing")
        return False
    fields = [tuple(fields[i:i + 2]) for i in range(0, len(fields), 2)]
    info = defaultdict(int)
    for vote, p_code in fields:
        if not vote.isnumeric():
            report_error(i, line, "Invalid Vote Count {}".format(vote))
            return False
        if p_code not in PARTY_CODE:
            report_error(i, line, "Invalid Party Code  {}".format(p_code))
            return False
        info[p_code] = int(vote)
    return info


def parse_feed(file):
    with open(file) as f:
        for i, line in enumerate(f.readlines()):
            constituency = extract_const(line, i)
            if not constituency: continue
            vote_info = extract_vote_info(line, i)
            if not vote_info: continue
            RESULTS[constituency].update(vote_info)


def display_result():
    for const, result in RESULTS.items():
        total = sum(result.values())
        print("{}(Total:{})".format(const, total))
        for p_code, vote in result.items():
            print("\t{}: {:.2%}".format(PARTY_CODE[p_code], float(vote) / float(total)))


try:
    parse_feed(FEED_FILE)
    display_result()
    print("Updating with override")
    parse_feed(OVERRIDE_FILE)
    display_result()
    save_error_log()
except Exception as e:
    save_error_log()
    raise e
