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

from .. import interface as I

        #how to solve this? need this methods?
#from pycoupler.coupler import Coupler

# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Environment.cells:
#from ...base import interface as B

# TODO: import those process types you need:
from .... import Step

import numpy as np

class Environment (I.Environment):
    """Environment process taxon mixin implementation class."""

    # standard methods:
    # TODO: remove those that you don't use 
    # TODO: use for initializing coupling

#     def __init__(self,
#                  # *,  # TODO: uncomment when adding named args after this
#                  **kwargs):
#         """Initialize the unique instance of Environment."""
#         super().__init__(**kwargs)  # must be the first line
#         # TODO: add custom code here
#         pass

    # process-related methods: 
    
    def next_update_step(self, t):
        return t + self.delta_t #given in study script?
    
    def LPJmL_copanCORE_coupling(self, t):
        
        input_data = self.in_dict #or skip this and directly write below
        year = self.end_year + t # TODO: check what t and year are and need to be
        
        ###need to make sure that copan core waits -> python works serial
           
        # send input data to lpjml
        #self.coupler.send_inputs(input_data, year)
 
        #read output data from lpjml
        #outputs = self.coupler.read_outputs(year)
        
        # TODO: check when input is set and what time output refers to,
        # beginning or end of year
        # beginning: prediction for whole year enables smoothing instead of annual jumps
        
        outputs = self.out_dict
        print(self.out_dict)
        outputs["cftfrac"] = np.ones((1, 32)) * input_data["landuse"][0,0]
        
        self.old_out_dict = self.out_dict
        self.out_dict = outputs # TODO: could be lpjml state at the end of the year, and old as beginning and then interpolate in cells
    



    # TODO: add what is needed for step process, for more cells distribute with for loop
    # dict variablen irgendwo einspeichern? VARIABLE_OF_INTEREST
    # allgemein eventuell too much (variable aus dict-key...) 
    # wir wissen ja, was von LPJmL kommt :) 

    processes = [Step("coupling step", 
        [I.Environment.out_dict], 
        [next_update_step, LPJmL_copanCORE_coupling])
    ]  # TODO: instantiate and list process objects here
