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

from pycopancore.models import social_inseeds as M


# paths
sim_path = "/p/projects/open/Jannes/copan_core/lpjml"
model_path = f"{sim_path}/LPJmL_internal"


startcell = 27410
endcell = 27418

# create config for coupled run
config_coupled = read_config(model_path=model_path, file_name="lpjml.js")

# set coupled run configuration
config_coupled.set_coupled(sim_path,
                           sim_name="coupled_test",
                           start_year=1901, end_year=2005,
                           coupled_year=1981,
                           coupled_input=["with_tillage"],
                           coupled_output=["soilc",
                                           "cftfrac",
                                           "pft_harvestc",
                                           "hdate"])

# only for single cell runs
config_coupled.outputyear = 1980
config_coupled.startgrid = startcell
config_coupled.endgrid = endcell
config_coupled.river_routing = False
config_coupled.tillage_type = "read"
config_coupled.double_harvest = False

config_coupled.add_config(
    "/p/projects/open/Jannes/copan_core/pycopancore/pycopancore/models/social_inseeds_config.yaml"  # noqa
)
config_coupled = config_coupled.coupled_config.aftpar.progressive_minded.weight_yield

# write config (Config object) as json file
config_coupled_fn = config_coupled.to_json()


# check if everything is set correct
check_lpjml(config_coupled_fn, model_path)

# run lpjml simulation for coupling in the background
run_lpjml(
    config_file=config_coupled_fn,
    model_path=model_path,
    sim_path=sim_path,
    std_to_file=False,  # write stdout and stderr to file
)

lpjml = LPJmLCoupler(config_file=config_coupled_fn)


world = M.World(lpjml=lpjml)

# instantiate the cells, when replaced with actual model, one could also pass
#    further entities to the cells, like the social system
# cells = world.init_cells(model=M)


farmers = world.init_individuals(model=M)
