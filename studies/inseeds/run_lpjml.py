"""Run script for InSEEDS with LPJmL coupling"""
import os
import numpy as np  # which is usually needed

from pycoupler.config import read_config
from pycoupler.run import run_lpjml, check_lpjml
from pycoupler.coupler import LPJmLCoupler
from pycoupler.utils import search_country

os.chdir("/p/projects/open/Jannes/copan_core/pycopancore")
# from pycopancore.runners.runner import Runner
from pycopancore.models import social_inseeds as M  # noqa


# Settings ================================================================== #

# paths
sim_path = "/p/projects/open/Jannes/copan_core/lpjml"
model_path = f"{sim_path}/LPJmL_internal"
inseeds_config_file = "/p/projects/open/Jannes/copan_core/pycopancore/pycopancore/models/social_inseeds_config.yaml"  # noqa"

spinup = True

# search for country code by supplying country name
# search_country("netherlands")
country_code = "NLD"

# Configuration ============================================================= #

# create config for spinup run
config_spinup = read_config(file_name="lpjml.js",
                            model_path=model_path,
                            spin_up=True)

# set spinup run configuration
config_spinup.set_spinup(sim_path)

# only for global runs = TRUE
config_spinup.river_routing = False

# regrid by country - create new (extracted) input files and update config
config_spinup.regrid(sim_path, country_code=country_code, overwrite_input=False)

# write config (Config object) as json file
config_spinup_fn = config_spinup.to_json()

# create config for historic run
config_historic = read_config(file_name="lpjml.js",
                                model_path=model_path)

# set historic run configuration
config_historic.set_transient(sim_path,
                                sim_name="historic_run",
                                dependency="spinup",
                                start_year=1901,
                                end_year=2000)

# only for global runs = TRUE
config_historic.river_routing = False
config_historic.tillage_type = "read"
config_historic.residue_treatment = "read_residue_data"

config_historic.double_harvest = False

# regrid by country - create new (extracted) input files and update config
config_historic.regrid(sim_path, country_code=country_code, overwrite_input=False)

# write config (Config object) as json file
config_historic_fn = config_historic.to_json()


# Simulations =============================================================== #

# check if everything is set correct
check_lpjml(config_file=config_spinup_fn)

# run spinup job
run_lpjml(
    config_file=config_spinup_fn
)

# check if everything is set correct
check_lpjml(config_historic_fn)

# run spinup job
run_lpjml(
    config_file=config_historic_fn
)
