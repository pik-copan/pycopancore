"""Test file for the simple extraction module."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license


import pycopancore.models.exploit as M

import numpy as np
import unittest

###################################################################
# Example from https://docs.python.org/3/library/unittest.html
###################################################################
# class TestStringMethods(unittest.TestCase):
#
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#         # self.assertTrue('Foo'.isupper(), "This test is failing on purpose.") #
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)


class TestSimpleExtraction(unittest.TestCase):

    def setUp(self):
        """called before any of the tests in this test case"""

        self.stock = np.random.random()
        self.growth_rate = np.random.random()
        self.strategy = np.random.random()

        self.culture = M.Culture()
        self.world = M.World(culture=self.culture)
        self.cell = M.Cell(stock=self.stock, capacity=1, growth_rate=self.growth_rate, world=self.world)
        self.individual = M.Individual(
            strategy=self.strategy,
            imitation_tendency=0,
            cell=self.cell
        )

    def test_simple_extractiont(self):
        """Check the whole component."""
        #######################################################
        # Put all tests in one method, else you might get
        # annoying problems because we have a global list
        # of instances for most classes.
        #######################################################
        # self.assertTrue(False, "This is definitely wrong")
        solution = 0.5 * self.growth_rate * (3 - 2 * self.strategy) * self.stock
        self.assertEqual(self.individual.get_harvest_rate(), solution)