import os
import argparse

from pycoupler.coupler import LPJmLCoupler
from pycopancore.models import social_inseeds as M


def run_inseeds(config_coupled_fn):

    if not os.path.exists(config_coupled_fn):
        raise FileNotFoundError(f"{config_coupled_fn} does not exist")

    lpjml = LPJmLCoupler(config_file=config_coupled_fn)

    world = M.World(model=M, lpjml=lpjml)

    farmers = world.init_individuals()

    for year in world.lpjml.get_sim_years():
        world.update(year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_coupled_fn", help="path to the config file")
    args = parser.parse_args()

    run_inseeds(args.config_coupled_fn)

# execute program via
# python inseeds.py /path/to/config_coupled_fn.json
