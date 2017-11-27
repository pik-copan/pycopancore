"""ODE process class.

ODE stands for Ordinary Differential Equation.
ODEs are used for continuos processes in which one of the targets is
dependent of the time.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

#
# Imports
#


#
# Definition of class ODE
#

from ..private import _AbstractProcess


class ODE(_AbstractProcess):
    """Define ODE process class."""

    type = "ODE"
    timetype = "continuous"

    def __init__(self,
                 name,
                 targets,
                 specification,
                 *,
                 smoothness=1
                ):
        """Instantiate an instance of an ODE process.

        Parameters
        ----------
        name : string
        targets : list
            list of Variables or _AttributeReferences whose time derivatives
            are added to by specification
        specification : func, or list of Expr
            function(self,t) storing the derivatives in instance
            attributes d_varname, or list of sympy expressions giving the
            RHS of the equation(s)
        smoothness
        """
        super().__init__(name)

        self.targets = targets
        self.specification = specification
        self.smoothness = smoothness
