"""A class to define model variables and inherits from Symbol.

Each Varible is connected to an entity, of which it is a variable.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

from sympy import Symbol

#
# Define class Variable
#


class Variable(Symbol):
    """Define the Variable Class."""

    owning_classes = []
    _codename = None

    # Do this init when enough time, now it's only creating problems
    # def __init__(self):
    #    super().__init__()
    #    self.owning_class = []

    def set_values(self,
                   *,
                   dict=None,
                   instances=None,
                   values=None
                   ):
        """Set values for the variable.

        This function set values for the variable. If given a list of
        instances, it sets values for all of them.

        Parameters
        ----------
        dict : dict
            Optional dictionary of variable values keyed by Entity
            object (e.g. {cell:location, individual:age},...)
        instances : list
            List of the instances, e.g. Cells or Process Taxa Objects
        values : list/array
            Optional corresponding list or array of values

        Returns
        -------

        """
        if dict is not None:
            for (e, val) in dict.items():

                #
                # Following assert statements need _AbstractEntityMixin. We
                # maybe should move them into the test environment:
                # assert isinstance(e, _AbstractEntityMixin), /
                # "key is not a model entity"
                # assert self._codename in e.__dict__, /
                # "variable is not contained in entity"
                #

                e.__dict__[self._codename] = val

        if instances is not None:
            for i in range(len(instances)):
                # Items may be entities or process taxa objects
                item = instances[i]

                #
                # as above...
                # assert isinstance(e, _AbstractEntityMixin). /
                # "key is not a model entity"
                # assert self._codename in e.__dict__, /
                # "variable is not contained in entity"
                #

                item.__dict__[self._codename] = values[i]

    def clear_derivatives(self,
                          *,
                          instances=None
                          ):
        """Set all derivatives to zero.

        Parameters
        ----------
        instances : list
            List of the instances, e.g. Cells or Process Taxa Objects

        Returns
        -------

        """
        for item in instances:
            item.__dict__['d_'+self._codename] = 0

    def get_derivatives(self,
                        *,
                        instances=None
                        ):
        """Return a list of derivatives saved in instances.

        Parameters
        ----------
        instances : list
            List of the instances, e.g. Cells or Process Taxa Objects

        Returns
        -------

        """
        return[item.__dict__['d_'+self._codename] for item in instances]

    def get_value_list(self,
                       instances=None,
                       ):
        """Return values for given instances.

        Parameters
        ----------
        instances : list
            List of the instances, e.g. Cells or Process Taxa Objects

        Returns
        -------
        List of variable value of each entity
        """
        return [item.__dict__[self._codename] for item in instances]
