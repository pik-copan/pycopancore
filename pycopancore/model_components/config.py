"""Config module for configuring generic components such as generic_imitation.
In any model definition using a component that needs configuration, 
first import this module and set its attributes 
before (!) importing the respective component(s).

Example:

from ..model_components import config
from ...model_components import environmental_awareness as aware
...
config.generic_imitation = {'variables': [aware.interface.Individual.is_environmentally_friendly]}
from ...model_components import generic_imitation as imi
...
"""

variables = None
"""list of Variable objects that will be imitated in the model"""
