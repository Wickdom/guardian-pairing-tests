#!/usr/bin/env python
class InvalidInput(Exception):
    pass


def staff_managers(ifile):
    staff_mgrs = {}
    with open(ifile, 'r') as f:
        for line in f:
            if line.strip():
                record = line.split()
                if len(record) != 2:
                    raise InvalidInput("Input file has an invalid record: {}".format(record))
                staff_mgrs.setdefault(*record)
    return staff_mgrs


def parse_args():
    import sys, os

    if len(sys.argv) != 4:
        print("Usage: ./staff staff.input Brenda Andrea")
        sys.exit(1)

    ifile = sys.argv[1]

    if not os.path.isfile(ifile):
        raise InvalidInput("Unable to locate a file by name {} under {}".format(ifile, os.path.abspath(os.path.curdir)))

    return ifile, sys.argv[2], sys.argv[3]


def find_arbitrator(ifile, staff1, staff2):
    sm_dict = staff_managers(ifile)

    def _validate_staff(name):
        if name not in sm_dict and name not in sm_dict.values():
            raise InvalidInput("Staff name {} not found in Staff records".format(name))
        return name

    _validate_staff(staff1)
    _validate_staff(staff2)

    def _immediate_mgrs(s1, s2):
        return sm_dict.get(s1, s1), sm_dict.get(s2, s2)

    manager1, manager2 = _immediate_mgrs(staff1, staff2)

    s1_mgrs = set([])
    s2_mgrs = set([])

    def _find_common_mgr():
        if manager1 in s2_mgrs:
            return manager1
        if manager2 in s1_mgrs:
            return manager2

    while manager1 != manager2:
        common_mgr = _find_common_mgr()
        if common_mgr:
            return common_mgr
        s1_mgrs.add(manager1)
        s2_mgrs.add(manager2)

        staff1, staff2 = manager1, manager2
        manager1, manager2 = _immediate_mgrs(staff1, staff2)

    return manager1


def main():
    ifile, staff1, staff2 = parse_args()
    print(find_arbitrator(ifile, staff1, staff2))


if __name__ == "__main__":
    main()
