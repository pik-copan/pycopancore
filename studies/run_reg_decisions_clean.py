"""Test run script for LPJmL coupling"""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
import os
os.chdir("/p/projects/copan/users/lschwarz/core/pycopancore")

import pycopancore.models.social_inseeds as M

# from pycopancore.models import social_inseeds as M

# standard runner for simulating any model:
from pycopancore.runners.runner import Runner

from pycopancore import master_data_model as D  # to be able to specify variables with physical units

import numpy as np  # which is usually needed
from numpy.random import choice, uniform  # to generate random initial conditions

import pylab as plt  # to plot stuff

# instantiate the model and have it analyse its own structure:
model = M.Model()


# # coupled simulation years
start_year = 1981
end_year = 2005


delta_t = 1  # desired temporal resolution of the resulting output.

test_dict_in = {"with_tillage": np.zeros((1, 1), dtype=int)}
test_dict_out = {"cftfrac": np.zeros((1, 32)), "pft_harvestc": np.zeros((1, 32))}

landuse_update_rate = 10
landuse_update_prob = 1.


dt = 1  # desired temporal resolution of the resulting output.


# instantiate process taxa:
env = M.Environment(
    delta_t=delta_t,  # dt should be given to environment probably
    start_year=start_year,  # our starting point
    in_dict=test_dict_in,
    out_dict=test_dict_out,
    old_out_dict=test_dict_out,
    # coupler=coupler
    )
met = M.Metabolism(
    landuse_update_rate=landuse_update_rate,
    landuse_update_prob=landuse_update_prob
    )
cul = M.Culture(
    )

# generate entities:

world = M.World(
    environment=env,
    metabolism=met,
    culture=cul,
    )
soc = M.SocialSystem(world=world)
cell = M.Cell(
    social_system=soc,
    lpjml_grid_cell_ids=[0],
    # landuse = test_dict_in["landuse"][0]
    # with_tillage=test_dict_in["with_tillage"][0],
    )
ind = M.Individual(cell=cell)

# Run the model
#

runner = Runner(model=model)
traj = runner.run(t_0=start_year, t_1=end_year, dt=dt)

# TODO: Add some further analysis such as plotting or saving
# plt.plot(traj['t'], traj[M.SocialSystem.population][socs[0]])
# plt.show()

# coupler.close_channel()
