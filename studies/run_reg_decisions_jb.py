"""Test run script for LPJmL coupling"""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
import os
os.chdir("/p/projects/open/Jannes/copan_core/pycopancore")

import numpy as np  # which is usually needed
from pycoupler.config import read_config
from pycoupler.run import run_lpjml
from pycoupler.coupler import LPJmLCoupler
from pycoupler.utils import check_lpjml

from pycopancore.model_components import lpjml as L
# import warnings
# warnings.filterwarnings("error")

# import pycopancore.models.social_inseeds as M
# # standard runner for simulating any model:
# from pycopancore.runners.runner import Runner
# # to be able to specify variables with physical units
# from pycopancore.data_model import master_data_model as D

# paths
sim_path = "/p/projects/open/Jannes/copan_core/lpjml"
model_path = f"{sim_path}/LPJmL_internal"


startcell = 27410
endcell = 27418

# create config for coupled run
config_coupled = read_config(model_path=model_path, file_name="lpjml.js")

# set coupled run configuration
config_coupled.set_coupled(sim_path,
                           start_year=1901, end_year=2005,
                           coupled_year=1981,
                           coupled_input=["with_tillage",
                                          "landuse"],
                           coupled_output=["soilc",
                                           "pft_harvestc",
                                           "leaching"])

# only for single cell runs
config_coupled.outputyear = 1980
config_coupled.startgrid = startcell
config_coupled.endgrid = endcell
config_coupled.river_routing = False
config_coupled.tillage_type = "read"

# write config (Config object) as json file
config_coupled_fn = config_coupled.to_json()


# check if everything is set correct
check_lpjml(config_coupled_fn, model_path)

# run lpjml simulation for coupling in the background
run_lpjml(
    config_file=config_coupled_fn,
    model_path=model_path,
    sim_path=sim_path
)

lpjml = LPJmLCoupler(config_file=config_coupled_fn)


# TODO: L is only a temporary solution, should be replaced by the actual model
world = L.World(lpjml=lpjml)
# instantiate the cells, when replaced with actual model, one could also pass
#    further entities to the cells, like the social system
cells = world.init_cells(model=L)

# instantiate the model and have it analyse its own structure:
model = M.Model()

delta_t = 1  # desired temporal resolution of the resulting output.


# test_dict_in = {"landuse": np.zeros((1, 64)),"fertilizer_nr": np.zeros((1, 32))}
# test_dict_out = {"cftfrac": np.zeros((1, 32)),"pft_harvestc": np.zeros((1, 32)),"pft_harvestn": np.zeros((1, 32))}


# adjust reading and writing as in Jannes' test script
# erst mal benötigt als pre-struktur, kommt dann quasi weg, wenn lpjml output da ist
# fkt die output auf hohem level als argument entgegennimmt
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

# world = M.World(
#     environment=env,
#     metabolism=met,
#     culture=cul,
# )
soc = M.SocialSystem(world=world)

cells = world.init_cells(model=L)

ind = M.Individual(cell=cell)

# Run the model
#

runner = Runner(model=model)
traj = runner.run(t_0=start_year, t_1=end_year, dt=dt)

# TODO: Add some further analysis such as plotting or saving
# plt.plot(traj['t'], traj[M.SocialSystem.population][socs[0]])
# plt.show()

# coupler.close_channel()
