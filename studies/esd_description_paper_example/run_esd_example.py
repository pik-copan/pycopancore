"""Script to run model that is presented in the esd description paper."""

from time import time
import argparse
import pickle
import numpy as np
import pycopancore.models.example2 as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

NUMBER_SOCIAL_SYSTEMS = 2
NUMBER_CELLS = 4
NUMBER_INDIVIDUALS = 400
RENEWABLE_SCALING = 2500000
FINAL_TIME = 2120


def run(seed, updates, with_social, p_env_friendly):
    """Run the model."""

    np.random.seed(seed)

    if with_social:
        filename = "esd_example_with_social_update_rate_{0}_seed_{1}.p".format(
            updates, seed
        )
    else:
        filename = "esd_example_without_social_seed_{0}.p".format(seed)

    model = M.Model()

    # instantiate process taxa:
    environment = M.Environment()
    metabolism = M.Metabolism(renewable_energy_knowledge_spillover_fraction=0)

    culture = M.Culture(
        awareness_lower_carbon_density=1e-5,
        awareness_upper_carbon_density=4e-5,
        awareness_update_rate=updates * with_social,
        environmental_friendliness_learning_rate=updates * with_social,
    )

    # generate entities and plug them together:
    world = M.World(
        environment=environment,
        metabolism=metabolism,
        culture=culture,
        atmospheric_carbon=830 * D.gigatonnes_carbon,
        upper_ocean_carbon=(5500 - 830 - 2480 - 1125) * D.GtC,
    )

    social_systems = []
    for _ in range(NUMBER_SOCIAL_SYSTEMS):
        _soc = M.SocialSystem(
            world=world,
            has_renewable_subsidy=False,
            has_emissions_tax=False,
            has_fossil_ban=False,
            emissions_tax_intro_threshold=1,
            renewable_subsidy_intro_threshold=0.5,
            fossil_ban_intro_threshold=0.5,
            renewable_subsidy_keeping_threshold=0.5,
            fossil_ban_keeping_threshold=0.5,
            emissions_tax_level=20 * 200e9,
            time_between_votes=4 if with_social else 1e100,
        )
        social_systems.append(_soc)

    cells = []
    for cell_id in range(NUMBER_CELLS):
        _cell = M.Cell(
            social_system=social_systems[cell_id // 2],
            renewable_sector_productivity=[0.7, 0.9, 1.1, 1.3][cell_id]
            * RENEWABLE_SCALING
            * M.Cell.renewable_sector_productivity.default,
            fossil_sector_productivity=(
                M.Cell.fossil_sector_productivity.default * 280
            ),
            biomass_sector_productivity=3e5 * 10 ** (0.4) * 900,
        )
        cells.append(_cell)

    individuals = []
    for individual_id in range(NUMBER_INDIVIDUALS):
        _individual = M.Individual(
            cell=cells[individual_id % 4],
            is_environmentally_friendly=np.random.choice(
                [False, True], p=[1 - p_env_friendly, p_env_friendly]
            ),
        )
        individuals.append(_individual)

    # initialize block model acquaintance network:
    # 2.5% of all agents. Dunbar's number would be too large
    target_degree = 10
    target_degree_samecell = 0.5 * target_degree
    target_degree_samesoc = 0.35 * target_degree
    target_degree_other = 0.15 * target_degree
    p_samecell = target_degree_samecell / (
        NUMBER_INDIVIDUALS / NUMBER_CELLS - 1
    )
    p_samesoc = target_degree_samesoc / (
        NUMBER_INDIVIDUALS / NUMBER_SOCIAL_SYSTEMS
        - NUMBER_INDIVIDUALS / NUMBER_CELLS
        - 1
    )
    p_other = target_degree_other / (
        NUMBER_INDIVIDUALS - NUMBER_INDIVIDUALS / NUMBER_SOCIAL_SYSTEMS - 1
    )
    for index, i in enumerate(individuals):
        for j in individuals[:index]:
            if i.cell == j.cell:
                prop = p_samecell
            elif i.social_system == j.social_system:
                prop = p_samesoc
            else:
                prop = p_other

            if np.random.uniform() < prop:
                culture.acquaintance_network.add_edge(i, j)

    # distribute area and vegetation uniformly since it seems there are no real
    # differences between the actual zones:
    sigma_0 = 1.5e8 * D.square_kilometers * np.array([0.25, 0.25, 0.25, 0.25])
    M.Cell.land_area.set_values(cells, sigma_0)

    # 2480 is yr 2000
    l_0 = 2480 * D.gigatonnes_carbon * np.array([0.25, 0.25, 0.25, 0.25])
    M.Cell.terrestrial_carbon.set_values(cells, l_0)

    # distribute fossils linearly from north to south, 1125 is yr 2000:
    g_0 = 1125 * D.gigatonnes_carbon * np.array([0.4, 0.3, 0.2, 0.1])
    M.Cell.fossil_carbon.set_values(cells, g_0)

    # distribute population 1:3 between north and south, 6e9 is yr 2000:
    # r = np.random.uniform(size=nsocs)
    p_0 = 6e9 * D.people * np.array([0.25, 0.75])
    M.SocialSystem.population.set_values(social_systems, p_0)

    # distribute capital 2:1:
    k_0 = sum(p_0) * 1e4 * D.dollars / D.people * np.array([2 / 3, 1 / 3])
    M.SocialSystem.physical_capital.set_values(social_systems, k_0)

    s_0 = 2e11 * D.gigajoules * np.array([1, 1])
    M.SocialSystem.renewable_energy_knowledge.set_values(social_systems, s_0)

    # do simulation:
    runner = Runner(model=model)
    starttime = time()
    traj = runner.run(
        t_0=2000,
        t_1=FINAL_TIME,
        dt=1,
        add_to_output=[M.Individual.represented_population],
    )

    save(traj=traj, filename=filename)
    print("Runtime:", time() - starttime, " seconds")


def save(traj, filename):
    tosave = {}
    for key in traj.keys():
        if key == "t":
            tosave["t"] = traj[key]
        else:
            data = {str(e): traj[key][e] for e in traj[key].keys()}
            tosave[key.owning_class.__name__ + "." + key.codename] = data
    pickle.dump(tosave, open(filename, "wb"))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--task-id", type=int)
    parser.add_argument("-u", "--update-rate", type=float)
    parser.add_argument(
        "-p",
        "--initial-share-enviromentally-friendly",
        default=0.25,
        type=float,
    )
    parser.add_argument("-s", "--seed", default=0, type=int)
    parser.add_argument(
        "--with-social", action="store_const", const=True, default=False
    )
    args = vars(parser.parse_args())

    print(args)
    seed = args["seed"]
    with_social = args["with_social"]
    p_env_friendly = args["initial_share_enviromentally_friendly"]

    if args["update_rate"]:
        updates = args["update_rate"]
    elif args["task_id"] is not None:
        updates = np.logspace(np.log10(1 / 50), np.log10(12), 50)[
            args["task_id"]
        ]
    elif not with_social:
        updates = 0
    else:
        assert False, "Either task-id oder update rate must be given."

    run(seed, updates, with_social, p_env_friendly)


if __name__ == "__main__":
    main()
