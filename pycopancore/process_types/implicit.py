"""Implicit proccess class.

Implicit functions are not yet implemented.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
# Imports
#


#
# Definition of class Event
#

from ..private import _AbstractProcess


class Implicit(_AbstractProcess):
    """Define the class Implicit."""

    type = "Implicit"
    timetype = "discrete" # ???

    def __init__(self,
                 name,
                 targets,
                 specification
                ):
        """Instantiate an instance of an implicit process.

        # TODO: Implement symbolic expressions
        Parameters
        ----------
        name: str
            Name of the Process
        variables: list
            list of variables that are altered by the process
        specification: method
            method that depends on the variables and must return zero
        """
        super().__init__(name)

        assert callable(specification), 'only callable implicits are implemented yet, is {}'.format(type(specification))

        self.targets = targets
        self.specification = specification
