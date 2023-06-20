"""
Cell entity type mixing class template.

TODO: adjust, uncomment or fill in code and documentation wherever marked by
the "TODO" flag.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from .. import interface as I
import numpy as np
# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Cell.individuals:
# from ...base import interface as B

# TODO: import those process types you need:
# from .... import Explicit, ODE, Event, Step


class Cell (I.Cell):
    """Cell entity type mixin implementation class."""
    pass

    processes = []