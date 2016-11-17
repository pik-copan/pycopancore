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
# Definition of class ODE
#

from pycopancore.private import _AbstractProcess


class ODE(_AbstractProcess):
    """
    Time-continuous process represented by a (system of) ordinary differential
    equation(s).
    """

    type = "ODE"
    timetype = "continuous"

    def __init__(self,
                 name,
                 variables,
                 specification,
                 smoothness=1,
                 ):
        """
        :param name: string
        :param variables: list of Variables whose time derivatives are added
               to by specification
        :param specification: function(t) storing the derivatives in instance
               attributes d_varname, or list of sympy expressions giving the
               RHS of the equation(s)
        :param smoothness:
        """
        super(ODE, self).__init__()

        self.name = name
        self.variables = variables
        self.specification = specification
        self.smoothness = smoothness
