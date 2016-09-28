# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Encapsulates states and dynamics of local environmental stocks.
"""

#
#  Imports
#
from .abstract_local_stocks import LocalStocks
import numpy as np


#
#  Define class LocalStocks
#

class simple_local_stocks(LocalStocks):
    """
    Encapsulates states and dynamics of global environmental stocks.
    """

    #
    #  Definitions of internal methods
    #

    #
    #  Definitions of further methods
    #

    def resource_function(capacity, starting_value, growthrate, time):
        """
        Function which returns amount of the renewable resource in dependece of
        the capcity, the starting value, the growthrate and time based on
        logistic growth
        """
        G = capacity
        f_0 = starting_value
        k = growthrate
        t = time
        R = G / (1 + np.exp(-k * G * t) * ((G / f_0) - 1))
        return R
