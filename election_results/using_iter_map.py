import os
from collections import defaultdict


FEED_DIR = os.path.abspath(".")
FEED_FILE = os.path.join(FEED_DIR, 'feed.txt')
FEED_ERR = os.path.join(FEED_DIR, 'feed_err.txt')
OVERRIDE_FILE = os.path.join(FEED_DIR, 'override.txt')

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


class FeedErr(Exception):
    pass


def report_error(line_no, line, f_err):
    err = "Line No: {}\nEntry: {}\nIssue: {}\n{}".format(line_no + 1, line.strip(), str(f_err), "-" * 80)
    # print(err)
    ERRORS.append(err)


def save_error_log():
    with open(FEED_ERR, 'w+') as ef:
        ef.write("\n".join(ERRORS))


def validate(line):
    if line.startswith('#') or line is None:
        raise FeedErr(line, "Comment or Empty Line")
    if ',' not in line:
        raise FeedErr(line, "Expected delimeter ',' not found in the line")


def parse_line(line):
    validate(line)
    fields = line.split(',')

    const = fields.pop(0)
    if const.isnumeric():
        raise FeedErr("Invalid Constituency value {}".format(const))

    if len(fields) == 0:
        raise FeedErr("Result info is missing")
    if len(fields) % 2:
        raise FeedErr("Vote or Party Code missing; Expect to be found in pairs")

    itr = [iter(fields)] * 2

    def translate_p_v(v, p):
        try:
            party = PARTY_CODE[p.strip()]
        except KeyError as e:
            raise FeedErr("Incorrect Party Code {}".format(e.args[0]))
        try:
            vc = int(v.strip())
        except ValueError:
            raise FeedErr("Position of Vote/Party Code inter changed or incorrect value for Vote found")

        if vc < 0:
            raise FeedErr("Invalid Vote Count {} for Party {}".format(vc, party))
        return party, vc

    p_vote = list(map(translate_p_v, *itr))
    return const, p_vote


def parse_feed(file):
    with open(file) as f:
        for i, line in enumerate(f):
            try:
                constituency, vote_info = parse_line(line)
                RESULTS[constituency].update(vote_info)
            except FeedErr as f_err:
                report_error(i, line, f_err)


def display_result():
    for const, result in RESULTS.items():
        total = sum(result.values())
        print("{}(Total:{})".format(const, total))
        for party, vote in result.items():
            print("\t{}: {:.2%}".format(party, float(vote) / float(total)))

def display_updates():
    print("\nUpdates:")
    print('Islington South & Finsbury > Labour Party vote changed  to {}'.format(
                                                                                        RESULTS[
                                                                                            'Islington South & Finsbury'][
                                                                                            'Labour Party']))
    print(RESULTS['Cardiff West']['Independent'], 'votes added to Cardiff West > Independent')


if __name__ == "__main__":

    try:
        parse_feed(FEED_FILE)
        display_result()
        print("\nUpdating with override\n")
        parse_feed(OVERRIDE_FILE)
        display_result()
        display_updates()
        save_error_log()
    except Exception as e:
        save_error_log()
        raise e
