# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Constructing basic functions that will be needed in each model.
"""

#
#  Imports
#

#
#  Define class abstract_model
#


class Model(object):
    """
    Constructing basic functions that will be needed in each model.
    """

    #
    # Definitions of internal methods
    #

    def __init__(self):
        """
        Initialize an instance of abstract_model.
        """

    def __str__(self):
        """
        Return a string representation of the object of class model
        """

    #
    # Definitions of further methods
    #

    def setup(self, components):
        """
        A function to allocate the ingredients (tuples of dynamics) of each
        class in a corresponding list of specified logictype.

        Parameters
        ----------
        components : dict
            A dictionary with class objects as values and corresponding
            abbrevations as keys (e.g. components = {"CUL":Culture(), ...})
        """
        self.components = components

        # Generate a list that unifies the ingredients of all classes
        self.ingredients = []
        for component in self.components.values(): 
            self.ingredients += component.get_ingredients()
            
        # Collect ingredients by logictype

        self.explicit_funcs = []
#        self.explicit_syms = []
        self.explicit_vars = []
#        self.implicit_funcs = []
#        self.implicit_syms = []
        self.derived_funcs = []
#        self.derived_syms = []
        self.derived_vars = []
        self.ODE_funcs = []
#        self.ODE_syms = []
        self.ODE_vars = []
        self.events_rate_fixed = []
#        self.events_rate_funcs = []
#        self.events_rate_syms = []
        self.events_time_funcs = []
        self.step_immediate = []
#        self.step_linear = []
#        self.step_delayed = []

        # Evaluation of each tuple in the ingredients list and allocation to
        # corresponding logictype list
        for item in self.ingredients:

            label, logictype, variables  = item[:3]

            if logictype == "event":
                eventtype = item[3]
                dofunc = item[5]
                
                if eventtype == "time":
                    timefunc = item[4]
                    self.events_time_funcs.append(item)
                
                elif eventtype == "rate":
                    ratespec = item[4]

                    if hasattr(ratespec, "__call__"):
                        ratetype = "func"
                    else:

                        if type(ratespec) == type(1.):
                            ratetype = "fixed"
                            self.events_rate_fixed.append(item)
                        else:
                            ratetype = "sym"
            
            elif logicype == "step":
                steptype = item[3]

                if steptype == "immediate":
                    self.step_immediate.append(item)

            else:
                spec = item[3]
                if hasattr(spec,"__call__"):
                    spectype = "func"
                else:
                    spectype = "sym"

                if logictype == "explicit":
                    self.explicit_funcs.append(item)
                    for var in variables:
                        self.explicit_vars.append(var)

                elif logictype == "derived":
                    self.derived_funcs.append(item)

                elif logictype == "ODE":
                    self.ODE_funcs.append(item)
                    for var in variables:
                        self.ODE_variables.append(variables)
