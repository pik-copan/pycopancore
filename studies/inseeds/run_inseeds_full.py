"""Run script for InSEEDS with LPJmL coupling"""
import os
import numpy as np  # which is usually needed

from pycoupler.config import read_config
from pycoupler.run import run_lpjml
from pycoupler.coupler import LPJmLCoupler
from pycoupler.utils import check_lpjml, search_country

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

# Spinup run ---------------------------------------------------------------- #
if spinup:
    # create config for spinup run
    config_spinup = read_config(file_name="lpjml.js",
                                model_path=model_path,
                                spin_up=True)

    # set spinup run configuration
    config_spinup.set_spinup(sim_path)

    # set more recent input files
    config_spinup.radiation = "cloudiness"
    config_spinup.input.temp.name = "CRU_TS4.03/cru_ts4.03.1901.2018.tmp.clm"
    config_spinup.input.prec.name = "CRU_TS4.03/cru_ts4.03.1901.2018.pre.clm"
    config_spinup.input.cloud.name = "CRU_TS4.03/cru_ts4.03.1901.2018.cld.clm"
    config_spinup.input.co2.name = "input_VERSION2/co2_1841-2018.dat"
    config_spinup.input.wetdays.name = "CRU_TS4.03/cru_ts4.03.1901.2018.wet.clm"  # noqa
    config_spinup.input.landuse.name = "input_toolbox_30arcmin/cftfrac_1500-2017_64bands_f2o.clm"  # noqa

    # only for global runs = TRUE
    config_spinup.river_routing = False

    # regrid by country - create new (extracted) input files and update config
    config_spinup.regrid(sim_path, country_code=country_code, overwrite_input=True)

    # write config (Config object) as json file
    config_spinup_fn = config_spinup.to_json()

    # create config for historic run
    config_historic = read_config(file_name="lpjml.js",
                                  model_path=model_path)

    # set historic run configuration
    config_historic.set_transient(sim_path,
                                  sim_name="historic_run",
                                  start_year=1901,
                                  end_year=2000)

    # set more recent input files
    config_historic.radiation = "cloudiness"
    config_historic.input.temp.name = "CRU_TS4.03/cru_ts4.03.1901.2018.tmp.clm"
    config_historic.input.prec.name = "CRU_TS4.03/cru_ts4.03.1901.2018.pre.clm"
    config_historic.input.cloud.name = "CRU_TS4.03/cru_ts4.03.1901.2018.cld.clm"  # noqa
    config_historic.input.co2.name = "input_VERSION2/co2_1841-2018.dat"
    config_historic.input.wetdays.name = "CRU_TS4.03/cru_ts4.03.1901.2018.wet.clm"  # noqa
    config_historic.input.landuse.name = "input_toolbox_30arcmin/cftfrac_1500-2017_64bands_f2o.clm"  # noqa

    # only for global runs = TRUE
    config_historic.river_routing = False
    config_historic.tillage_type = "read"
    config_historic.double_harvest = False

    # regrid by country - create new (extracted) input files and update config
    config_historic.regrid(sim_path, country_code=country_code, overwrite_input=True)

    # write config (Config object) as json file
    config_historic_fn = config_historic.to_json()


# Coupled run --------------------------------------------------------------- #

# create config for coupled run
config_coupled = read_config(model_path=model_path, file_name="lpjml.js")

# set coupled run configuration
config_coupled.set_coupled(sim_path,
                           sim_name="coupled_test",
                           start_year=2001, end_year=2050,
                           coupled_year=2023,
                           coupled_input=["with_tillage"],
                           coupled_output=["soilc_agr_layer",
                                           "cftfrac",
                                           "pft_harvestc",
                                           "hdate",
                                           "country",
                                           "region"])

# only for single cells runs
config_coupled.outputyear = 2022

# set more recent input files
config_coupled.radiation = "cloudiness"
config_coupled.input.temp.name = "CRU_TS4.03/cru_ts4.03.1901.2018.tmp.clm"
config_coupled.input.prec.name = "CRU_TS4.03/cru_ts4.03.1901.2018.pre.clm"
config_coupled.input.cloud.name = "CRU_TS4.03/cru_ts4.03.1901.2018.cld.clm"
config_coupled.fix_co2 = True
config_coupled.fix_co2_year = 2018
config_coupled.input.co2.name = "input_VERSION2/co2_1841-2018.dat"
config_coupled.input.wetdays.name = "CRU_TS4.03/cru_ts4.03.1901.2018.wet.clm"  # noqa
config_coupled.input.landuse.name = "input_toolbox_30arcmin/cftfrac_1500-2017_64bands_f2o.clm"  # noqa
config_coupled.fix_climate = True
config_coupled.fix_climate_cycle = 11
config_coupled.fix_climate_year = 2013

# only for global runs = TRUE
config_coupled.river_routing = False
config_coupled.tillage_type = "read"
config_coupled.residue_treatment = "no_residue_remove"  # "read_residue_data"
config_coupled.double_harvest = False

# regrid by country - create new (extracted) input files and update config file
config_coupled.regrid(sim_path, country_code=country_code, overwrite_input=True)

config_coupled.add_config(inseeds_config_file)

# write config (Config object) as json file
config_coupled_fn = config_coupled.to_json()


# Simulations =============================================================== #

# LPJmL spinup run ---------------------------------------------------------- #
if spinup:
    # check if everything is set correct
    check_lpjml(config_file=config_spinup_fn, model_path=model_path)

    # run spinup job
    run_lpjml(
        config_file=config_spinup_fn,
        model_path=model_path,
        sim_path=sim_path
    )

    # check if everything is set correct
    check_lpjml(config_file=config_historic_fn, model_path=model_path)

    # run spinup job
    run_lpjml(
        config_file=config_historic_fn,
        model_path=model_path,
        sim_path=sim_path
    )

# LPJmL coupled run --------------------------------------------------------- #

# check if everything is set correct
check_lpjml(config_coupled_fn, model_path)

# run lpjml simulation for coupling in the background
run_lpjml(
    config_file=config_coupled_fn,
    model_path=model_path,
    sim_path=sim_path,
    std_to_file=False,  # write stdout and stderr to file
)

# InSEEDS run --------------------------------------------------------------- #

# establish coupler connection to LPJmL
lpjml = LPJmLCoupler(config_file=config_coupled_fn)

# initialize (LPJmL) world
world = M.World(model=M, lpjml=lpjml)

# initialize (cells and) individuals
farmers, cells = world.init_individuals()

# run coupled model until end_year
for year in world.lpjml.get_sim_years():
    world.update(year)
