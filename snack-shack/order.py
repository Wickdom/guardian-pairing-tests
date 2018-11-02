from pprint import pprint
from datetime import datetime,timedelta


SCHEDULE = []
SANDWICH_TASKS = [("make", 60), ("serve", 30)]
MAX_WAIT_TIME = 5*60

def display_schedule():
    for info in SCHEDULE:
        print("{}:{:02}".format(*divmod(info["start"], 60)), info["task"], "sandwich", info["order"])
        # print(info["order_at"]+timedelta(seconds=info["start"]), info["task"], "sandwich", info["order"])


def order(no_of_sw):
    for sw in range(1, no_of_sw + 1):
        for task, time in SANDWICH_TASKS:
            start = 0
            if SCHEDULE:
                start = SCHEDULE[-1]["finish"]
            finish = start + time
            if finish > MAX_WAIT_TIME:
                print("Sorry! too busy we can't take orders now")
                return
            task_info = {"order": sw,
                         "start": start,
                         "finish": finish,
                         "task": task}
            SCHEDULE.append(task_info)
        if start:
            print("Your order will be served in: {} min {} secs".format(*divmod(start, 60)))



order(4)
display_schedule()