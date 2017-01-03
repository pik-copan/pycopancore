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
import inspect

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
        # super(Model, self).__init__(**kwargs)

        self.all_entities = kwargs['entities']

        # Is the following necessary?
        # Check this classes' entities and make them part of itself. Now this
        # is just a dirty workaround, need clean solution for future!
        subclass = Cell.__subclasses__()[0]
        self.cells = self.all_entities[subclass]

        print('     dummy model instantiated')

    def __repr__(self):
        """
        Return a string representation of the object of class dummy.Model.
        """
        return (super().__repr__() +
                ('dummy.model object with cells %r '
                 ) % (self.cells)
                )
