"""Run script for InSEEDS with LPJmL coupling"""
from pycoupler.config import read_config
from pycoupler.run import run_lpjml, check_lpjml
from pycoupler.coupler import LPJmLCoupler
from pycoupler.utils import search_country

# from pycopancore.runners.runner import Runner
from pycopancore.models import social_inseeds as M  # noqa


# Settings ================================================================== #

# paths
sim_path = "./copan_core/nl_runs"
model_path = "./copan_core/lpjml/LPJmL_internal"
inseeds_config_file = "./copan_core/pycopancore/pycopancore/models/social_inseeds_config.yaml"  # noqa"

# search for country code by supplying country name
# search_country("netherlands")
country_code = "NLD"

# Configuration ============================================================= #

# create config for coupled run
config_coupled = read_config(
    model_path=model_path, file_name="lpjml_config.cjson"
)

# set coupled run configuration
config_coupled.set_coupled(sim_path,
                           sim_name="coupled_test",
                           dependency="historic_run",
                           start_year=2001, end_year=2100,
                           coupled_year=2023,
                           coupled_input=["with_tillage"],  # residue_on_field
                           coupled_output=["soilc_agr_layer_fast",
                                           "cftfrac",
                                           "pft_harvestc",
                                           "hdate",
                                           "country",
                                           "region",
                                           "terr_area"])

# only for single cells runs
config_coupled.outputyear = 2022

config_coupled.fix_co2 = True
config_coupled.fix_co2_year = 2022
config_coupled.fix_climate = True
config_coupled.fix_climate_cycle = 11
config_coupled.fix_climate_year = 2013

# only for global runs = TRUE
config_coupled.river_routing = False

config_coupled.tillage_type = "read"
config_coupled.residue_treatment = "read_residue_data"
config_coupled.double_harvest = False

# regrid by country - create new (extracted) input files and update config file
config_coupled.regrid(
    sim_path,
    country_code=country_code,
    overwrite_input=False
)

config_coupled.add_config(inseeds_config_file)

# set InSEEDS configuration: here we set the progressive probability to 0.25
config_coupled.coupled_config.progressive_probability = 0.25

# write config (Config object) as json file
config_coupled_fn = config_coupled.to_json()


# Simulations =============================================================== #

# check if everything is set correct
check_lpjml(config_coupled_fn)

# run lpjml simulation for coupling in the background
run_lpjml(
    config_file=config_coupled_fn,
    std_to_file=False  # write stdout and stderr to file
)

# InSEEDS run --------------------------------------------------------------- #

# establish coupler connection to LPJmL
lpjml = LPJmLCoupler(config_file=config_coupled_fn)

# initialize (LPJmL) world
world = M.World(model=M, lpjml=lpjml)

# initialize (cells and) individuals
farmers, cells = world.init_individuals()

for year in world.lpjml.get_sim_years():
    world.update(year)
