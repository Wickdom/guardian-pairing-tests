from pprint import pprint
from datetime import datetime, timedelta
import json

SCHEDULE = []
ITEM_TASK_INFO = {'s': [("make", 60), ("serve", 30)],
                  'j': [("make", 60), ("serve", 30)],
                  }

MAX_WAIT_TIME = 5 * 60
INVENTORY_FILE = "inventory.json"
INVENTORY = {}


def retrieve_inventory():
    global INVENTORY
    with open(INVENTORY_FILE, "r") as f:
        INVENTORY = json.loads(f.read())
    return INVENTORY


def update_inventory():
    with open(INVENTORY_FILE, "w") as f:
        f.write(json.dumps(INVENTORY))


def display_inventory():
    print("Inventory Check: We can make max no of the following items")
    for i, n in INVENTORY.items():
        print("{} {}".format(n, item_name(i)))


def display_schedule():
    for info in SCHEDULE:
        print("{}:{:02}".format(*divmod(info["start"], 60)), info["task"], item_name(info["item"]), info["order"])
        # print(info["order_at"]+timedelta(seconds=info["start"]), info["task"], "sandwich", info["order"])


def item_name(code):
    return {'s': "Sandwich",
            'j': "Jacket Potato"}[code]


def order(no, item='s'):
    item_tasks = ITEM_TASK_INFO[item]
    retrieve_inventory()
    for order_no in range(1, no + 1):
        if INVENTORY[item] < 1:
            print("Sorry! {} is SOLD OUT".format(item_name(item)))
            break
        start = 0
        if SCHEDULE:
            start = SCHEDULE[-1]["finish"]
        tasks = []
        for task, time in item_tasks:
            finish = start + time
            if finish > MAX_WAIT_TIME:
                print("Sorry! too busy can't take more orders")
                update_inventory()
                return
            tasks.append({"order": order_no,
                          "item": item,
                          "start": start,
                          "finish": finish,
                          "task": task})
            start = finish
        SCHEDULE.extend(tasks)
        INVENTORY[item] -= 1

        print("item_name(item) {} will be served in: {} min {} secs".format(order_no, *divmod(start, 60)))

    update_inventory()



order(4)
display_schedule()
display_inventory()

