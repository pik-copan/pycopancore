"""Cell entity type mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
# from .... import master_data_model as D


class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 stock=100,
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)
        self.stock = stock


    # process-related methods:

    processes = []
