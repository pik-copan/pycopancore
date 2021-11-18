"""Script to run example2 model."""

from time import time
from numpy import random, array
import numpy as np
import pandas as pd
import networkx as nx

import pycopancore.models.example2 as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show, figure, subplot, gca, semilogy, legend

from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

# first thing: set seed so that each execution must return same thing:
random.seed(10)

# parameters:

nworlds = 1  # no. worlds
nsocs = 248 # no. social_systems  # TODO: Später auf Ländercluster aus Sophie Spilles Arbeit reduzieren.
ncells = 248  # no. cells  # TODO: Später mit Luana abstimmen wegen LPJ. Alternativ: Zellen aus Sophie Spilles Arbeit verwenden.
ninds = 1000 # no. individuals  # TODO: 10000 wie bei Nils

t_1 = 2000.2

# choose one of two scenarios:
with_social = 0  # 0 or 1

# directory to store results:
dump_dir = "/tmp/"

# choose one of two scenarios:
with_socials = 0 # 0 or 1

if with_socials == 1:
    filename = dump_dir + "with.pickle" # (this file will be read by plot_jobst2leander.py)
    with_awareness = 1
    with_learning = 1
    with_voting = 1
else:
    filename = dump_dir + "without.pickle"
    with_awareness = 0
    with_learning = 0
    with_voting = 0

print("Using model as defined in file", M.__file__)
model = M.Model()
runner = Runner(model=model)

# read in countries data
data_folder = "leanders_model/data/"

usecols = ["mw_numeric", "area", "population", "gdp", "gdi"]
countries_df = pd.read_csv(data_folder + "country_data.csv", usecols = usecols)

country_ids_list = countries_df.mw_numeric.to_numpy()
country_ids_reverse_dict = {country_ids_list[i]: i for i in range(len(country_ids_list))}

# read in nodeset from Nils
nodesets_folder = "leanders_model/codevonnils/Output_Nodesets/"

nodeset_data = np.load(nodesets_folder + "nodeset_0.npz")
node_country_array = nodeset_data['arr_4']
node_elevation_array = nodeset_data['arr_3']

# read in network from Nils
networks_folder = "leanders_model/codevonnils/Output_Networks/"

network_data = np.load(networks_folder + "network_0.npz")
adjacency_matrix = network_data['arr_0']
node_is_potentially_active_array = network_data['arr_1']

# instantiate process taxa:
environment = M.Environment()

metabolism = M.Metabolism(
    renewable_energy_knowledge_spillover_fraction = 0
    )

culture = M.Culture(
    awareness_lower_carbon_density=1e-4,
    awareness_upper_carbon_density=2e-4,
    awareness_update_rate = 1 if with_awareness else 0,
    environmental_friendliness_learning_rate = 1 if with_learning else 0,
    acquaintance_network = nx.from_numpy_matrix(adjacency_matrix), # adding Nils' network already here
    )

# generate entities and plug them together:
(world, ) = worlds = [M.World(
    environment = environment, 
    metabolism = metabolism, 
    culture = culture,
    atmospheric_carbon = 830 * D.gigatonnes_carbon,
    upper_ocean_carbon = (5500 - 830 - 2480 - 1125) * D.GtC
    ) for w in range(nworlds)]

# TODO: Distinguish further? give all of these a name?
social_systems = [M.SocialSystem(
    world = world,
    has_renewable_subsidy = False,
    has_emissions_tax = False,
    has_fossil_ban = False,
    emissions_tax_intro_threshold = 0.5, # disabled
    renewable_subsidy_intro_threshold = 1, # disabled
    fossil_ban_intro_threshold = 1, # disabled
    emissions_tax_level = 30 * 200e9, # see Wikipedia social cost of carbon. 100e9*3.5,
    time_between_votes = 4 if with_voting else 1e100, 
    ) for s in range(nsocs)]

# TODO: Change productivities of each country?
cells = [M.Cell(
    social_system = social_systems[c],
    renewable_sector_productivity = 0.1 * M.Cell.renewable_sector_productivity.default,
        # represents dependency of solar energy on solar insolation angle TODO reimplement! 
    fossil_sector_productivity =  80 * M.Cell.fossil_sector_productivity.default,
    biomass_sector_productivity =  60 * M.Cell.biomass_sector_productivity.default
    # these values result in realistic total energy production for the year 2000, see below  # TODO: anpassen, so dass die Gesamtenergieprod. wieder stimmt, s.u.
    ) for c in range(ncells)]

# TODO: hier die Variable is_environmentally_friendly stattdessen gemäß Nils' "certainly active" nodes ersetzen:
# TODO: Nils uses only elevation but not distance to coast??
individuals = [M.Individual(
                cell = cells[country_ids_reverse_dict[node_country_array[i]]], # assign cell according to id from nodeset
                is_environmentally_friendly = 
                    random.choice([False, True], p=[.8, .2]), # represents the "20% suffice" assumption 
                ) 
               for i in range(ninds)]

# read in land area and distribute vegetation accordingly since it seems there are no real differences between the actual zones:
# WARNING: this is still total area
area_per_country = countries_df.area.to_numpy()
Sigma0 = area_per_country * D.square_kilometers
M.Cell.land_area.set_values(cells, Sigma0)

L0 = 2480 * area_per_country/sum(area_per_country) * D.gigatonnes_carbon  # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)
M.Cell.mean_past_terrestrial_carbon.set_values(cells, L0)

# distribute fossils linearly from north to south:
G0 = 1125 * area_per_country/sum(area_per_country) * D.gigatonnes_carbon  # 1125 is yr 2000
M.Cell.fossil_carbon.set_values(cells, G0)

# read in population distribution from Nils' input data:
population_per_country = countries_df.population.to_numpy()
P0 = population_per_country * D.people # total of 7.77e9
M.SocialSystem.population.set_values(social_systems, P0) #WARNING before we had read in an array of length 4 here for nsocs=2 with no errors

# read in gdp (for some countries this is just scaled up average per capita gdp, see data generation):
gdp_per_country = countries_df.gdp.to_numpy()
gdi_per_country = countries_df.gdi.to_numpy()
K0 = gdi_per_country * D.dollars
M.SocialSystem.physical_capital.set_values(social_systems, K0)

# everybody knows the same about renewables:
S0 = 1e12 * D.gigajoules * np.ones(nsocs)
M.SocialSystem.renewable_energy_knowledge.set_values(social_systems, S0)

w = worlds[0]
s = social_systems[0]
c = cells[0]
for v in environment.variables: print(v,v.get_value(environment))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))


def get_initial_state():
    return { 
        etpt: { 
            v: { 
                i: v.get_value(i) 
                for i in etpt.instances } 
            for v in etpt.variables } 
        for etpt in [M.Cell, M.Culture, M.Environment, M.Individual, M.Metabolism, M.SocialSystem, M.World] }

def set_initial_state(x0):
    for etpt, vardict in x0.items():
        for v, instancedict in vardict.items():
            if not v.readonly:
                v.set_values(list(instancedict.keys()), list(instancedict.values()))

x0 = get_initial_state()


from scipy.optimize import fmin


# set sector productivities that roughly match real-world energy production:

print("\n\n\nFITTING SECTOR PRODUCTIVITIES...")

Rtarget = 100 * D.gigawatts / (D.gigajoules / D.years)

def target(productivities):
    print("\n\nTRYING PRODUCTIVITIES",productivities,":\n")
    set_initial_state(x0)
    M.Cell.biomass_sector_productivity.set_values(cells, np.ones(ncells) * productivities[0])
    M.Cell.fossil_sector_productivity.set_values(cells, np.ones(ncells) * productivities[1])
    M.Cell.renewable_sector_productivity.set_values(cells, np.ones(ncells) * productivities[2])
    traj = runner.run(t_0=2000, t_1=2000.001, dt=1)
    Bglobal = sum(traj[M.SocialSystem.biomass_input_flow][s][1] for s in social_systems)
    Fglobal = sum(traj[M.SocialSystem.fossil_fuel_input_flow][s][1] for s in social_systems)
    Rglobal = sum(traj[M.SocialSystem.renewable_energy_input_flow][s][1] for s in social_systems)  # D.gigajoules / D.years
    err = ((Bglobal - 3)/3)**2 + ((Fglobal - 11)/11)**2 + ((Rglobal - Rtarget)/Rtarget)**2
    print("\nERROR:", err)
    return err
    
productivities0 = np.array([3e5, 5e6, 7e-18])
print("START:",productivities0)
productivities = fmin(target, productivities0)
print("OPTIMAL:",productivities)
set_initial_state(x0)
M.Cell.biomass_sector_productivity.set_values(cells, np.ones(ncells) * productivities[0])
M.Cell.fossil_sector_productivity.set_values(cells, np.ones(ncells) * productivities[1])
M.Cell.renewable_sector_productivity.set_values(cells, np.ones(ncells) * productivities[2])

"""
# set initial capital values that roughly match a certain GDP distribution:

print("\n\n\nFITTING INITIAL CAPITAL...")

GWP_2000 = 33.57e12  # gross world product in 2000 in USD

# for illustration, use a random GDP distribution (later use real-world data):
r = random.uniform(size=nsocs)
Ytargets = GWP_2000 * r / r.sum()

def target2(logcapitals):
    capitals = np.exp(logcapitals)
    print("\n\nTRYING CAPITALS",capitals,":\n")
    set_initial_state(x0)
    M.SocialSystem.physical_capital.set_values(social_systems, capitals)
    traj = runner.run(t_0=2000, t_1=2000.001, dt=1)
    err = ((np.array(M.SocialSystem.economic_output_flow.get_values(social_systems)) - Ytargets)**2).sum()
    print("\nERROR:", err)
    return err
    
capitals0 = np.array(M.SocialSystem.physical_capital.get_values(social_systems))
capitals = np.exp(fmin(target2, np.log(capitals0)))
print("START:",capitals0)
print("OPTIMAL:",capitals)
set_initial_state(x0)
M.SocialSystem.physical_capital.set_values(social_systems, capitals)
"""


# do simulation:
start = time()
traj = runner.run(t_0=2000, t_1=t_1, dt=1, 
                  add_to_output=[   M.Individual.represented_population,
                                    M.Cell.mean_past_terrestrial_carbon, 
                                    M.SocialSystem.population
                                    ]
                  )

for v in environment.variables: print(v,v.get_value(environment))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))


from pickle import dump
tosave = {
          v.owning_class.__name__ + "."
          + v.codename: {str(e): traj[v][e]
                         for e in traj[v].keys()
                         } 
          for v in traj.keys() if v is not "t"
          }
tosave["t"] = traj["t"]
dump(tosave, open(filename,"wb"))
print(time()-start, " seconds")

t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

B0 = sum(traj[M.SocialSystem.biomass_input_flow][s][5] 
         for s in social_systems)
Bglobal = B0 * D.gigatonnes_carbon / D.years
Fglobal = sum(traj[M.SocialSystem.fossil_fuel_input_flow][s][5] 
              for s in social_systems) * D.gigatonnes_carbon / D.years
Rglobal = sum(traj[M.SocialSystem.renewable_energy_input_flow][s][5] 
              for s in social_systems) * D.gigajoules / D.years
Eglobal = sum(traj[M.SocialSystem.secondary_energy_flow][s][5] 
              for s in social_systems) * D.gigajoules / D.years

print("B (3), F (11), R (30):",
      Bglobal, Bglobal.tostr(unit=D.gigatonnes_carbon/D.years),
      Fglobal, Fglobal.tostr(unit=D.gigatonnes_carbon/D.years),
      Rglobal, Rglobal.tostr(unit=D.gigawatts),
      ) 

"""
# POSSIBLY TRY FITTING THESE VALUES AS WELL:
    
print("\nYr 2000 values (real):")
print("emigration (5e6):",sum(traj[M.SocialSystem.emigration][s][5] 
                              for s in social_systems)) # TODO: fit via changing basic_emigration_probability_rate
print("photo (123):",sum(traj[M.Cell.photosynthesis_carbon_flow][c][5] 
                         for c in cells)) # TODO: fit via changing cell's basic photosynthesis rate
print("resp (118):",sum(traj[M.Cell.terrestrial_respiration_carbon_flow][c][5] 
                        for c in cells)) # TODO: fit via changing cell's basic respiration rate
print("temp. at begin:", traj[M.World.surface_air_temperature][worlds[0]][5])
"""

