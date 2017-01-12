# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module the dummy model
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
                 **kwargs
                 ):
        """

        Parameters
        ----------
        kwargs
        """

        # Super does not need specification in python 3. Also,when this is not
        # called, base.model is not instantiated
        super().__init__(**kwargs)
        print('     dummy model instantiated')

    def __repr__(self):
        """
        Return a string representation of the object of class dummy.Model.
        """
        return (super().__repr__() +
                'dummy.model object')
