# This is the unittest to test te donut_world file and the DonutWorld class

# import unittest
# import numpy as np

from pycopancore import DonutWorld

DW = DonutWorld()

# First test to see if it works

def test_grid_shape():
    assert DW.grid.shape == (DW.height, DW.width)
