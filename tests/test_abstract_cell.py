# This is the first unittest to try out how it works!

# import unittest
# import numpy as np

from pycopancore import Cell

# check if the stocks variable is an array:


a = Cell(1)

assert(type(a.cell_identifier) == int)

assert(str(a.stocks[0, 1]) == 'nan')
