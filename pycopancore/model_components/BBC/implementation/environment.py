"""Enviroment process taxon mixing class template.

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
# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Environment.cells:
# from ...base import interface as B

# TODO: import those process types you need:
from .... import Explicit, ODE, Event
import numpy as np


class Environment(I.Environment):
    """Environment process taxon mixin implementation class."""

    processes = [
     ]