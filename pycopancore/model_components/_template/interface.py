"""Interface of model component AAA"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore import master_data_model as MDM # TODO: use variables from the master data model wherever possible
#from pycopancore import CFVariable, CETSVariable # TODO: uncomment if you need further variables from some catalogue
#import pycopancore.model_components.BBB.interface as BBB # TODO: uncomment and adjust of you need further variables from another model component
#from pycopancore import Variable # TODO: uncomment only if you really need other variables


class Model_(object):
    """Interface for Model mixin"""

    # metadata:
    name = "..." # a unique name for the model component
    description = "..." # some description
    requires = [] # list of other model components required for this model component to make sense


# entity types:

class World_(object):
    """Interface for World mixin"""

    # endogenous variables:
    #X = MDM.X # TODO: use variables from the master data model wherever possible wherever possible!
    #Y1 = CFVariable(ref="...") # TODO: uncomment and adjust if you need further variables from some catalogue
    #Y2 = CETSVariable(ref="...") # TODO: uncomment and adjust if you need further variables from some catalogue
    #Z = BBB.Z TODO: uncomment and adjust of you need further variables from another model component
    #W = Variable(name="W", unit=..., ...) # TODO: uncomment and adjust only if you really need other variables

    # exogenous variables / parameters:
    # TODO: similarly
    
class Cell_(object):
    """Interface for Cell mixin"""

    # endogenous variables:

    # exogenous variables / parameters:

class Individual_(object):
    """Interface for Individual mixin"""

    # endogenous variables:

    # exogenous variables / parameters:

class Society_(object):
    """Interface for Society mixin"""

    # endogenous variables:

    # exogenous variables / parameters:


# process taxa:

class Nature_(object):
    """Interface for Nature mixin"""

    # endogenous variables:

    # exogenous variables / parameters:

class Metabolism_(object):
    """Interface for Metabolism mixin"""

    # endogenous variables:

    # exogenous variables / parameters:

class Culture_(object):
    """Interface for Culture mixin"""

    # endogenous variables:

    # exogenous variables / parameters:
