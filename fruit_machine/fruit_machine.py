import random

SLOT = []
FLOAT_AMT = 10.0
BANK = FLOAT_AMT
PLAY_AMT = 0.20


def pick_color():
    return random.choice(['black', 'white', 'green', 'yellow'])


def roll():
    global SLOT
    SLOT = [pick_color(), pick_color(), pick_color(), pick_color()]


def prize():
    global BANK
    unique = set(SLOT)
    amt = 0
    credit = 0
    if len(unique) == 1:
        print("Congratulation!! You won JACKPOT", end='')
        amt = 1 * BANK
    elif len(unique) == 4:
        print("Congratulation!! You won 1/2 JACKPOT", end='')
        amt = 1 * BANK
    elif SLOT[0] == SLOT[1] or SLOT[1] == SLOT[2] or SLOT[2] == SLOT[3]:
        print("Congratulation!! You won SPECIAL Prize", end='')
        a = BANK - 5 * PLAY_AMT
        if a >= 0:
            amt = 5 * PLAY_AMT
        else:
            amt = BANK
            credit = abs(a)
    else:
        print(":( Better Luck next time")

    BANK = max(BANK - amt, FLOAT_AMT)
    return amt, credit


def play():
    global BANK
    BANK += PLAY_AMT
    roll()
    print(SLOT)
    amt, credit = prize()
    if amt or credit:
        print(" worth of ",end='')
        if amt:
            print("£{:2.2f} cash payout".format(amt))
        if credit:
            print("£{:2.2f} play credits".format(credit))


if __name__ == '__main__':
    while True:
        play()
        print("-" * 80)
        input("Just hit to play £{:2.2f} worth of Jackpot for only £{:2.2f}!".format(BANK, PLAY_AMT))
