# This is the first unittest to try out how it works!

import unittest

from pycopacore import Cell
# Relative Imports are shit and do not work. So what now?

#check if the stocks variable is an array:

def array_test(stocks):
    assert(type(stocks) == np.array)
