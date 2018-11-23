
# Assumptions
1. There could be more than 2 reportees for a manager and a staff can skip one more level in hierarchy
  If not, binary search can be used
2. Top boss (root node) won't be explicitly defined in the input file
  If not, solution requires re-work
3. As it is company staff records, max size is less than or equal to Walmart size - 2,300,000
  If it is large, holding records dict may not be efficient.
4. There could be more than one input files.
  Otherwise, passing input file for every run wont be desirable

# For Improvements
Due to lack of time and considering the size of problem, the following are skipped
1. Test coverage
2. IO file operations can be patched in unit tests
3. separating tests code 
4. OS independent command line execution without .py extension

#Notes
0. Tested on MAC 10.14 / Python 3.7.0 & 2.7.15
1. A class based solution to avoid inner functions, is attached staff_class.py

