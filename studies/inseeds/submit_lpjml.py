"""Submit script for spinup and historic LPJmL simulations."""

from pycoupler.config import read_config
from pycoupler.run import check_lpjml, submit_lpjml

# Settings ================================================================== #

# paths
sim_path = "/p/projects/open/Jannes/copan_core/global_runs"
model_path = "/p/projects/open/Jannes/copan_core/lpjml/LPJmL_internal"


# Configuration ============================================================= #

# Spinup run ---------------------------------------------------------------- #

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

# write config (Config object) as json file
config_spinup_fn = config_spinup.to_json()


# Historic run -------------------------------------------------------------- #


# create config for historic run
config_historic = read_config(file_name="lpjml.js",
                              model_path=model_path)

# set historic run configuration
config_historic.set_transient(sim_path,
                              sim_name="historic_run",
                              dependency="spinup",
                              start_year=1901,
                              end_year=2000)

# set more recent input files
config_historic.radiation = "cloudiness"
config_historic.input.temp.name = "CRU_TS4.03/cru_ts4.03.1901.2018.tmp.clm"
config_historic.input.prec.name = "CRU_TS4.03/cru_ts4.03.1901.2018.pre.clm"
config_historic.input.cloud.name = "CRU_TS4.03/cru_ts4.03.1901.2018.cld.clm"
config_historic.input.co2.name = "input_VERSION2/co2_1841-2018.dat"
config_historic.input.wetdays.name = "CRU_TS4.03/cru_ts4.03.1901.2018.wet.clm"  # noqa
config_historic.input.landuse.name = "input_toolbox_30arcmin/cftfrac_1500-2017_64bands_f2o.clm"  # noqa


config_historic.tillage_type = "read"
config_historic.double_harvest = False

# write config (Config object) as json file
config_historic_fn = config_historic.to_json()


# Simulations =============================================================== #

# LPJmL spinup run ---------------------------------------------------------- #
# check if everything is set correct
check_lpjml(config_spinup_fn)

# run spinup job
submit_lpjml(
    config_file=config_spinup_fn,
    group="copan",
    wtime = "5:00:00"
)

# check if everything is set correct
check_lpjml(config_historic_fn)

# run spinup job
submit_lpjml(
    config_file=config_historic_fn,
    group="copan",
    wtime = "3:00:00"
)
