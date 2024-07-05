"""Submit script for spinup and historic LPJmL simulations."""

from pycoupler.config import read_config
from pycoupler.run import check_lpjml, submit_lpjml
from pycoupler.utils import search_country

# Settings ================================================================== #

# paths
sim_path = "./copan_core/global_runs"
model_path = "/copan_core/LPJmL_internal"


# Configuration ============================================================= #

# Spinup run ---------------------------------------------------------------- #

# create config for spinup run
config_spinup = read_config(file_name="lpjml.js",
                            model_path=model_path,
                            spin_up=True)

# set spinup run configuration
config_spinup.set_spinup(sim_path)


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

# management settings
config_historic.tillage_type = "read"
config_historic.residue_treatment = "read_residue_data"
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
    group="worldtrans",
    wtime = "1:00:00",
    ntasks=128
)

# check if everything is set correct
check_lpjml(config_historic_fn)

# run spinup job
submit_lpjml(
    config_file=config_historic_fn,
    group="worldtrans",
    wtime = "0:30:00",
    ntasks=128
)
