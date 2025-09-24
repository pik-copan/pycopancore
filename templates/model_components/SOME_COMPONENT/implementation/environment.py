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
# from .... import Explicit, ODE, Event, Step


class Environment(I.Environment):
    """Environment process taxon mixin implementation class."""

    # standard methods:
    # TODO: remove those that you don't use

    #     def __init__(self,
    #         # *,  # TODO: uncomment when adding named args after this
    #         **kwargs):
    #         """Initialize the unique instance of Environment."""
    #         super().__init__(**kwargs)  # must be the first line
    #         # TODO: add custom code here
    #         pass

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
