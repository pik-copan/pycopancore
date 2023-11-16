import os
import argparse

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

    # run coupled model until end_year
    for year in world.lpjml.get_sim_years():
        world.update(year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="Path to the configuration file")
    args = parser.parse_args()

    run_inseeds(args.config_file)

# execute program via
# python inseeds.py /path/to/config_coupled_fn.json
