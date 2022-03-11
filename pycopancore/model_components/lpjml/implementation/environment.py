"""Enviroment process taxon mixing class template.

TODO: adjust, uncomment or fill in code and documentation wherever marked by
the "TODO" flag.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from matplotlib.pyplot import step
from .. import interface as I

        #how to solve this? need this methods?
from pycoupler.coupler import Coupler

# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Environment.cells:
#from ...base import interface as B

# TODO: import those process types you need:
from .... import Step

class Environment (I.Environment):
    """Environment process taxon mixin implementation class."""

    # standard methods:
    # TODO: remove those that you don't use

#     def __init__(self,
#                  # *,  # TODO: uncomment when adding named args after this
#                  **kwargs):
#         """Initialize the unique instance of Environment."""
#         super().__init__(**kwargs)  # must be the first line
#         # TODO: add custom code here
#         pass

    # process-related methods: 
    
    def next_update_step(self, t):
        return t + self.dt #given in study script?
    
    def LPJmL_copanCORE_coupling(self, t):
        
        input_data = self.IN_DICT #or skip this and directly write below
        year = self.end_year + t
        
        ###need to make sure that copan core waits -> python works serial
           
        # send input data to lpjml
        self.coupler.send_inputs(input_data, year)
 
        # read output data from lpjml
        outputs = self.coupler.read_outputs(year)
        
        self.OUT_DICT = outputs
    



    # TODO: add what is needed for step process, for more cells distribute with for loop
    # dict variablen irgendwo einspeichern? VARIABLE_OF_INTEREST
    # allgemein eventuell too much (variable aus dict-key...) 
    # wir wissen ja, was von LPJmL kommt :) 

    processes = [step("coupling step",
        [I.Cell.OUT_DICT], 
        [next_update_step, LPJmL_copanCORE_coupling])
    ]  # TODO: instantiate and list process objects here
