"""model component Interface template

TODO: adjust or fill in code and documentation wherever marked by "TODO:", 
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# TODO: use variables from the master data model wherever possible:
from pycopancore import master_data_model as MDM 

# TODO: uncomment if you need further variables from some catalogue:
#from pycopancore import CFVariable, CETSVariable 

# TODO: uncomment and adjust of you need further variables 
# from another model component:
#import pycopancore.model_components.BBB.interface as BBB 

# TODO: uncomment only if you really need other variables:
#from pycopancore import Variable 


class Model_ (object):
    """Interface for Model mixin"""

    # metadata:
    name = "..." # a unique name for the model component
    description = "..." # some description
    # list of other model components required for this component to make sense:
    requires = [] 
    # Note: Model_ does NOT define variables or parameters, 
    # only entity types and process taxons do!


# entity types:

class World_ (object):
    """Interface for World mixin"""

    # endogenous variables:
    
    # TODO: use variables from the master data model wherever possible:
    #X = MDM.X 
    
    # TODO: uncomment/adjust if you need further variables from a catalogue:
    #Y1 = CFVariable(ref="...") 
    #Y2 = CETSVariable(ref="...")
    
    # TODO: uncomment/adjust of you need variables from another component:
    #Z = BBB.Z 
    
    # TODO: uncomment and adjust only if you really need other variables:
    #W = Variable(name="W", unit=..., ...) 

    # exogenous variables / parameters:
    # TODO: similarly
    
class Society_ (object):
    """Interface for Society entity type mixin"""

    # endogenous variables:

    # exogenous variables / parameters:

class Cell_ (object):
    """Interface for Cell entity type mixin"""

    # endogenous variables:

    # exogenous variables / parameters:

class Individual_ (object):
    """Interface for Individual entity type mixin"""

    # endogenous variables:

    # exogenous variables / parameters:


# process taxa:

class Nature_ (object):
    """Interface for Nature process taxon mixin"""

    # endogenous variables:

    # exogenous variables / parameters:

class Metabolism_ (object):
    """Interface for Metabolism process taxon mixin"""

    # endogenous variables:

    # exogenous variables / parameters:

class Culture_ (object):
    """Interface for Culture process taxon mixin"""

    # endogenous variables:

    # exogenous variables / parameters:
