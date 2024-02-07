import os
import argparse
from pyinstrument import Profiler

from pycoupler.coupler import LPJmLCoupler
from pycopancore.models import social_inseeds as M


def run_inseeds(config_file):

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"{config_file} does not exist")

    # establish coupler connection to LPJmL
    lpjml = LPJmLCoupler(config_file)

    # initialize (LPJmL) world
    world = M.World(model=M, lpjml=lpjml)

    # initialize (cells and) individuals
    farmers, cells = world.init_individuals()

    profiler = Profiler(interval=0.05)
    profiler.start()

    for year in world.lpjml.get_sim_years():
        if year == lpjml.config.lastyear:
            profiler.stop()
            profiler.write_html(
                f"/p/projects/open/Jannes/copan_core/global_runs/profiler_{str(year)}.html"
            )
        world.update(year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="Path to the configuration file")
    args = parser.parse_args()

    run_inseeds(args.config_file)

# execute program via
# python inseeds.py /path/to/config_coupled_fn.json
