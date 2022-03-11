"""
Run script template.

TODO: Go through the file and adjust all parts of the code marked with the TODO
flag. Pay attention to those variables and objects written in capital letters.
These are placeholders and must be adjusted as needed. For further details see
also the model development tutorial.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
 
import pycopancore.models._testing.lpjml.lpjml_dummy as M  # TODO: adjust

# standard runner for simulating any model:
from pycopancore.runners.runner import Runner

from pycopancore import master_data_model as D  # to be able to specify variables with physical units

import numpy as np  # which is usually needed
from numpy.random import choice, uniform  # to generate random initial conditions

import pylab as plt  # to plot stuff

# instantiate the model and have it analyse its own structure:
model = M.Model()

#
# TODO: All necessary model setup, such as setting initial conditions or
# instantiating taxa and entities, comes after this line and before the next
# commented block below. The following code is exemplary:
#

#include config of LPJmL (maybe in own .py)    
#from pycoupler.coupler import Coupler
#from pycoupler.data import supply_inputs, preprocess_inputs
 
 
# paths
base_path = "/p/projects/open/Jannes/copan_core/lpjml_test"
config_coupled_fn = f"{base_path}/config_coupled.json"
 
# coupled simulation years
start_year = 1981
end_year = 2005
sim_years = range(start_year, end_year+1)
 
# initiate coupler after run_lpjml on LOGIN NODE 1
#coupler = Coupler(config_file=config_coupled_fn)
 
# get and process initial inputs
#inputs = supply_inputs(config_file=config_coupled_fn,
                       #historic_config_file=config_historic_fn,
                       #input_path=f"{base_path}/input",
                       #model_path=model_path,
                       #start_year=start_year, end_year=start_year)
#input_data = preprocess_inputs(inputs, grid=coupler.grid, time=start_year)

# simulation parameters:

dt = 1  # desired temporal resolution of the resulting output.
 
# TODO ? dt_lpjml = dt*12 #adjust temporal scales?
 
end_year = 2005
test_dict_in = {"landuse": np.random.rand(1, 64),"fertilizer_nr": np.random.rand(1, 32)}
test_dict_out = {"cftfrac": np.random.rand(1, 32),"pft_harvestc": np.random.rand(1, 32),"pft_harvestn": np.random.rand(1, 32)}

t_max = 100  # interval for which the model will be simulated
# dt = 0.1  # desired temporal resolution of the resulting output.


# instantiate process taxa:
env = M.Environment(
    dt = dt, #dt should be given to environment probably
    end_year = end_year, #our starting point
    in_dict = test_dict_in,
    out_dict = test_dict_out
    )
met = M.Metabolism(
    )
cul = M.Culture(
    )

# generate entities:

world = M.World(
    environment = env,
    metabolism = met,
    culture = cul,
    # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
    )  # TODO: in case of many worlds, make a list
soc = M.SocialSystem(world = world)
cell = M.Cell(
    social_system = soc,
    cftfrac = test_dict_out["cftfrac"][0],
    landuse = test_dict_in["landuse"][0]
    )
ind = M.Individual(cell = cell)

# Run the model
#

runner = Runner(model=model)
traj = runner.run(t_0=0, t_1=t_max, dt=dt)

# TODO: Add some further analysis such as plotting or saving
# plt.plot(traj['t'], traj[M.SocialSystem.population][socs[0]])
# plt.show()
