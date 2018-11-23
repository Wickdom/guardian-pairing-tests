import unittest
import os
import sys

from staff import InvalidInput, find_arbitrator, parse_args
from nose.tools import assert_equal, assert_raises, assert_true


class TestParseArgs(unittest.TestCase):

    def test_valid_cmd_line_args(self):
        sys.argv = ["prog", "test_staff.input", "Staff1", "Staff2"]
        ifile, staff1, staff2 = parse_args()
        assert_equal((ifile, staff1, staff2), tuple(sys.argv[1:]))

    def test_incomplete_cmd_line_args(self):
        sys.argv = ["prog", "only_file"]
        with assert_raises(SystemExit):
            parse_args()

    def test_more_than_4_inputs(self):
        sys.argv = ["prog", "test_staff.input", "Staff1", "Staff2", "Extra"]
        with assert_raises(SystemExit):
            parse_args()

    def test_invalid_file(self):
        sys.argv = ["prog", "file_not_exists", "Adam", "Bob"]
        with assert_raises(InvalidInput) as context:
            parse_args()
        assert_true("Unable to locate" in str(context.exception))


class TestFindArbitrator(unittest.TestCase):
    def setUp(self):
        self.ifile = os.path.join(os.path.dirname(__file__), "test_staff.input")

    def test_staffs_under_same_manager(self):
        assert_equal("B1", find_arbitrator(self.ifile, "A1", "A2"))

    def test_non_existant_staff(self):
        with assert_raises(InvalidInput) as context:
            find_arbitrator(self.ifile, "Unknown", "A1")
        assert_true("not found in Staff records" in str(context.exception))

    def test_non_existing_manager(self):
        with assert_raises(InvalidInput) as context:
            find_arbitrator(self.ifile, "A1", "Unknown")
        assert_true("not found in Staff records" in str(context.exception))

    def test_a_manager_own_reporting_line_as_other_staff(self):
        assert_equal(find_arbitrator(self.ifile, "A1", "C1"), "D1")

    def test_non_reporting_manager_as_staff(self):
        assert_equal(find_arbitrator(self.ifile, "A1", "B3"), "D1")

    def test_staff_manager_same(self):
        assert_equal(find_arbitrator(self.ifile, "A1", "A1"), "B1")

    def test_root_as_another_staff(self):
        assert_equal(find_arbitrator(self.ifile, "A1", "F1"), "F1")

    def test_root_as_both_staff_manager(self):
        assert_equal(find_arbitrator(self.ifile, "F1", "F1"), "F1")

    def test_staff_from_less_level_hirearchy(self):
        assert_equal(find_arbitrator(self.ifile, "C3", "A3"), "F1")

    def test_invalid_record_in_file(self):
        self.ifile = os.path.join(os.path.dirname(__file__), "invalid_record.input")
        with assert_raises(InvalidInput) as context:
            find_arbitrator(self.ifile, "E1", "F1")
        assert_true("Input file has an invalid" in str(context.exception))


if __name__ == "__main__":
    unittest.main()