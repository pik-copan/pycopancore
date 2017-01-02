# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module a template for the Model mixing class is composed to give an
example of the basic structure of it. It inherits from Model_ in that variables
and parameters are defined.
"""

#
#  Imports
#

from .interface import Model_
from pycopancore.model_components import abstract
from . import Cell

#
#  Define class Model
#


class Model(Model_, abstract.Model):
    """
    A template for the basic structure of the Model mixin class that every model
    must use to compose their final Model class. Inherits from Model_ as the
    interface with all necessary variables and parameters.
    """

    #
    # Mixins
    #

    # Use Mixins as wanted

    entity_types = [Cell]
    process_taxa = []

    def __init__(self,
                 *,
                 cells=None,
                 **kwargs
                 ):
        """

        Parameters
        ----------
        kwargs
        """
        super(Model, self).__init__(**kwargs)

        self.cells = cells
        print('this is the dummy model, cells type=', type(self.cells))
