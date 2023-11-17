"""Submit script for InSEEDS with LPJmL coupling"""

from pycoupler.config import read_config
from pycoupler.run import check_lpjml, submit_lpjml


from pycopancore.models import social_inseeds as M  # noqa


# Settings ================================================================== #

# paths
sim_path = "/p/projects/open/Jannes/copan_core/global_runs"
model_path = "/p/projects/open/Jannes/copan_core/lpjml/LPJmL_internal"
inseeds_config_file = "/p/projects/open/Jannes/copan_core/pycopancore/pycopancore/models/social_inseeds_config.yaml"  # noqa"


# Configuration ============================================================= #

# create config for coupled run
config_coupled = read_config(model_path=model_path,
                             file_name="lpjml.js")

# set coupled run configuration
config_coupled.set_coupled(sim_path,
                           sim_name="coupled_test",
                           dependency="historic_run",
                           start_year=2001, end_year=2050,
                           coupled_year=2023,
                           coupled_input=["with_tillage"],  # residue_on_field
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

config_coupled.tillage_type = "read"
config_coupled.residue_treatment = "no_residue_remove"  # "read_residue_data"
config_coupled.double_harvest = False

config_coupled.add_config(inseeds_config_file)

# write config (Config object) as json file
config_coupled_fn = config_coupled.to_json()


# Simulations =============================================================== #

# check if everything is set correct
check_lpjml(config_coupled_fn)

# run lpjml simulation for coupling in the background
submit_lpjml(
    config_file=config_coupled_fn,
    couple_to="/p/projects/open/Jannes/copan_core/pycopancore/studies/inseeds/inseeds_main.py",
    group="copan",
    wtime = "3:00:00"
)
