from pprint import pprint

SCHEDULE = []
SANDWICH_TASKS = [("make", 60), ("serve", 30)]


def display_schedule():
    for info in SCHEDULE:
        print("{}:{:02}".format(*divmod(info["start"], 60)), info["task"], "sandwich", info["order"])


def order(no_of_sw):
    for sw in range(1, no_of_sw + 1):
        for task, time in SANDWICH_TASKS:
            start = 0
            if SCHEDULE:
                start = SCHEDULE[-1]["finish"]
            finish = start + time
            task_info = {"order": sw,
                         "start": start,
                         "finish": finish,
                         "task": task}
            SCHEDULE.append(task_info)

    display_schedule()


order(4)
