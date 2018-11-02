def divide_gems(chest, seekers):
    if chest is [] or seekers == 0:
        return False
    if seekers == 1:
        return chest

    total = sum(chest)
    share, rem = divmod(total, seekers)
    if rem:
        return False

    if len(set(chest)) == 1 and len(chest) == seekers:
        return [[chest[0]] * int((share / chest[0]))] * seekers

    chest.sort()

    if chest[-1] > share:
        return False

    partitions = [[] for _ in range(seekers)]

    def find_next_allocation():
        if not chest:
            return True

        gem = chest.pop()

        for i, allocated_gems in enumerate(partitions):
            allotment = sum(allocated_gems)
            new_allocation = allotment + gem
            if new_allocation <= share:
                partitions[i].append(gem)
                if allotment == share:
                    continue
                if find_next_allocation():
                    return True
                partitions[i].remove(gem)
                if not allotment:
                    break

        chest.append(gem)

        return False

    if find_next_allocation():
        return partitions


# assert f([27, 7, 20], 2) == [27], [20, 7]
# assert f([27, 7, 20], 3) == -1

tests = [

    [
        [4, 4, 4],
        3,
        [[4], [4], [4]]
    ],
    [
        [4, 4, 4, 4, 4, 4],
        3,
        [[4, 4], [4, 4], [4, 4]]
    ],
    [
        [4, 4, 4, 2, 2, 2],
        3,
        [[4, 2], [4, 2], [4, 2]]
    ],
    [
        [4, 4, 4, 2, 2, 2, 8, 7, 7, 1, 1],
        3,
        [[8, 4, 2], [7, 7], [4, 4, 2, 2, 1, 1]]
    ],
    [
        [4, 4, 4],
        4,
        False
    ],
    [
        [4, 4, 4, 3, 3, 3, 2, 2, 2],
        3,
        [[4, 3, 2]] * 3
    ],
    [
        [3, 2, 1, 3, 2, 1, 3, 2, 1],
        3,
        [[3, 3], [3, 2, 1], [2, 2, 1, 1]]
    ],
    [
        [1, 1, 2, 2, 3],
        3,
        [[3], [2, 1], [2, 1]]
    ],
    [
        [27, 7, 20],
        2, [[27], [20, 7]]
    ],
    [
        [27, 7, 20],
        3,
        False
    ],
]

tests1 = [
    [
        [4, 4, 4, 3, 3, 3, 2, 2, 2],
        3,
        [[2, 3, 4]] * 3
    ]
]

for chest, seekers, expected in tests:
    actual = divide_gems(chest.copy(), seekers)
    if actual != expected:
        print(" FAIL: Chest: {}, Seekers: {}; {} != {}".format(chest, seekers, actual, expected))
    else:
        print(" PASS: Chest: {}, Seekers: {}; {}".format(chest, seekers, actual))
