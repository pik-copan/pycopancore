"""Enviroment process taxon for LPJmL coupling component."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# TODO: implement actual coupling
from pycoupler.coupler import LPJmLCoupler

from pycopancore.process_types import Step

from .. import interface as I


class Environment (I.Environment):
    """Environment process taxon mixin implementation class."""

    # standard methods:
    # TODO: remove those that you don'time use
    # NOTE: can be used for initial coupling

    def __init__(self, *, lpjml=None, **kwargs):
        """Initialize the unique instance of Environment."""
        super().__init__(**kwargs)  # must be the first line
        self.lpjml = lpjml

    # process-related methods:
    def update(self, time):
        print("time right in the beginning: ", time)
        return time + self.delta_t

    # def LPJmL_copanCORE_coupling(self, time):
    #     print("start coupling year", time)
    #     input_data = self.in_dict  # or skip this and directly write below
    #     # idea: time should already be the year
    #     # currently dirty fix (time-1), as time apparently is already incremented
    #     # by the next_update_step process
    #     # TODO find a nicer way of doing this
    #     year = time-1
    #     print("running coupling year: ", year)
    #     # send input data to lpjml
    #     self.coupler.send_inputs(input_data, year)
    #     print("current year input values: ", input_data)
 # 
    #     # read output data from lpjml
    #     outputs = self.coupler.read_outputs(year)
    #     # TODO: check when input is set and what time output refers to,
    #     # beginning or end of year
    #     # beginning: prediction for whole year enables smoothing/interpolation instead of annual jumps
    #     
    #     # or: print(self.out_dict)
    #     print(outputs)
    #     # note: below was just to be able to see something in the coupling step
    #     # outputs = self.out_dict
    #     # outputs["cftfrac"] = np.ones((1, 32)) * input_data["with_tillage"][0,0]
    #     
    #     self.old_out_dict = self.out_dict  # save for interpolation of variables in cell or environment
    #     self.out_dict = outputs
    #     print(self.out_dict)

    # TODO: design decision: add read-out into cells already here, could be computationally more efficient, but less readable
    # TODO: add write-in already here
    # TODO coupler.close_channel()

    # processes = [Step("coupling step",
    #     [I.Environment.out_dict],
    #     [next_update_step, LPJmL_copanCORE_coupling])
    # ]

    processes = []
