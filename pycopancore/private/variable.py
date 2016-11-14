# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
A class to define model variables and inherits from Symbol. Each Varible
is connected to an entity, of which it is a variable.
"""

#
#  Imports
#

from sympy import Symbol

#
# Define class Variable
#


class Variable(Symbol):
    """
    A class to define model variables and inherits from Symbol. Each Varible
    is connected to an entity, of which it is a variable.
    """

    entity_type = None

    def set_values(self,
                   *,
                   dict=None,
                   entities=None,
                   values=None
                   ):
        """
        :param dict: Optional dictionary of variable values keyed by Entity
                     object (e.g. {cell:location, individual:age},...)
        :param entities: Optional list of entities (Cell, Individual,...)
        :param values: Optional corresponding list or array of values
        :return: -
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

            if entities is not None:
                for i in range(len(entities)):
                    e = entities[i]

                    #
                    # as above...
                    # assert isinstance(e, _AbstractEntityMixin). /
                    # "key is not a model entity"
                    # assert self._codename in e.__dict__, /
                    # "variable is not contained in entity"
                    #

                    e.__dict__[self._codename] = values[i]
