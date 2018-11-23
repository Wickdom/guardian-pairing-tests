#!/usr/bin/env python
class InvalidInput(Exception):
    pass


class StaffMgr:

    def __init__(self, ifile):
        self.staff_mgrs = self.sm_records(ifile)
        self.managers = self.staff_mgrs.values()
        self.staff1 = None
        self.staff2 = None

    @staticmethod
    def sm_records(ifile):
        staff_mgrs = {}
        with open(ifile, 'r') as f:
            for line in f:
                if line.strip():
                    record = line.split()
                    if len(record) != 2:
                        raise InvalidInput("Input file has an invalid record: {}".format(record))
                    staff_mgrs.setdefault(*record)
        return staff_mgrs

    def validated(self, name):
        if name not in self.staff_mgrs:
            if name not in self.managers:
                raise InvalidInput("Staff name {} not found in Staff records".format(name))
        return name

    def arbitration_for(self, s1, s2):
        self.staff1 = self.validated(s1)
        self.staff2 = self.validated(s2)

    def immediate_managers(self):
        return self.staff_mgrs.get(self.staff1, self.staff1), \
               self.staff_mgrs.get(self.staff2, self.staff2)

    def arbitrator(self):
        mgr1,mgr2 = self.immediate_managers()
        s2_mgrs = set([])
        s1_mgrs = set([])

        while mgr1 != mgr2:


            if mgr2 in s1_mgrs:
                return mgr2

            if mgr1 in s2_mgrs:
                return mgr1

            s1_mgrs.add(mgr1)
            s2_mgrs.add(mgr2)
            self.staff1 = mgr1
            self.staff2 = mgr2
            mgr1, mgr2 = self.immediate_managers()

        return mgr1

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
    SM = StaffMgr(ifile)
    SM.arbitration_for(staff1,staff2)
    return SM.arbitrator()


def main():
    ifile, staff1, staff2 = parse_args()
    arbitrator = find_arbitrator(ifile, staff1, staff2)
    print(arbitrator)


if __name__ == "__main__":
    main()