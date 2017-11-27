"""Skript to run Jobsts prototype model."""

from time import time
from numpy import random, array
import numpy as np
import pycopancore.models.jobsts_prototype_1 as M
# import pycopancore.models.only_copan_global_like_carbon_cycle as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show, figure, subplot, gca, semilogy, legend

# first thing: set seed so that each execution must return same thing:
random.seed(10) # 10

# parameters:

nworlds = 1  # no. worlds
nsocs = 5 # no. societies #10
ncells = 100  # no. cells #100
ninds = 1000 # no. individuals

model = M.Model()

# instantiate process taxa:
nature = M.Nature()
metabolism = M.Metabolism(
    renewable_energy_knowledge_spillover_fraction = .1, #.1, #.1,
        # 1 w/o protection: success but desertification
        # .75 w protection: success (even w/o or w much migration)
        # .1 w protection: success but desertification
        # 0 w/o protection: very slow success but desertification
        # ?: oscillations
    basic_emigration_probability_rate = 16e-13, # 5e-13 leads to ca. 5mio. at 10 socs, (real)
    )
culture = M.Culture(
    awareness_lower_carbon_density=1e-4, #1e100, # 1e-6?
    awareness_upper_carbon_density=2e-4, #1e100, # 2e-6?
    awareness_update_rate=0, #1:SUCCESS, #1e-10
    environmental_friendliness_learning_rate=0, #1:SUCCESS
    max_protected_terrestrial_carbon_share=0,
    )

# generate entities and plug them together at random:
worlds = [M.World(nature=nature, metabolism=metabolism, culture=culture,
                  atmospheric_carbon = 830 * D.gigatonnes_carbon,
                  upper_ocean_carbon = (5500 - 830 - 2480 - 1125) * D.gigatonnes_carbon
                  ) for w in range(nworlds)]
societies = [M.Society(world=random.choice(worlds),
                       has_renewable_subsidy = random.choice([False, True], p=[3/4, 1/4]), #True, #False,
                       has_emissions_tax = random.choice([False, True], p=[4/5, 1/5]), #True, #False,
                       has_fossil_ban = False, #True, #False,
                       time_between_votes = 1e100, #4, #1e100, # 4
                       ) for s in range(nsocs)]
cells = [M.Cell(society=random.choice(societies),
                renewable_sector_productivity = 2 * random.rand()
                    * M.Cell.renewable_sector_productivity.default)
         for c in range(ncells)]
individuals = [M.Individual(
                cell=random.choice(cells),
                is_environmentally_friendly = 
                    random.choice([False, True], p=[.7, .3]), #True, #False,
                ) 
               for i in range(ninds)]

# initialize block model acquaintance network:
target_degree = 150
target_degree_samecell = 0.5 * target_degree
target_degree_samesoc = 0.35 * target_degree
target_degree_other = 0.15 * target_degree
p_samecell = target_degree_samecell / (ninds/ncells - 1)
p_samesoc = target_degree_samesoc / (ninds/nsocs - ninds/ncells - 1)
p_other = target_degree_other / (ninds - ninds/nsocs - 1)
for index, i in enumerate(individuals):
    for j in individuals[:index]:
        if random.uniform() < (
                p_samecell if i.cell == j.cell 
                else p_samesoc if i.society == j.society \
                else p_other):
            culture.acquaintance_network.add_edge(i, j)
#print("degrees:",culture.acquaintance_network.degree())

# distribute area and vegetation randomly but correlatedly:
r = random.uniform(size=ncells)
Sigma0 = 1.5e8 * D.square_kilometers * r / sum(r)
M.Cell.land_area.set_values(cells, Sigma0)
# print(M.Cell.land_area.get_values(cells))

r += random.uniform(size=ncells)
L0 = 2480 * D.gigatonnes_carbon * r / sum(r)  # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)
# print(M.Cell.terrestrial_carbon.get_values(cells))

r = np.exp(random.normal(size=ncells))
G0 = 1125 * D.gigatonnes_carbon * r / sum(r)  # 1125 is yr 2000
M.Cell.fossil_carbon.set_values(cells, G0)
# print(M.Cell.fossil_carbon.get_values(cells))

r = random.uniform(size=nsocs)
P0 = 6e9 * D.people * r / sum(r)  # 500e9 is middle ages, 6e9 would be yr 2000
M.Society.population.set_values(societies, P0)
M.Society.migrant_population.set_values(societies, P0 * 250e6/6e9)
for s in societies:
    s.max_protected_terrestrial_carbon = 0.90 * sum(c.terrestrial_carbon for c in s.cells)

# print(M.Society.population.get_values(societies))
   
r = random.uniform(size=nsocs)
K0 = sum(P0) * 1e4 * D.dollars/D.people * r / sum(r)  # ?
M.Society.physical_capital.set_values(societies, K0)
# print(M.Society.physical_capital.get_values(societies))

# for renewables, do NOT divide by number of socs:    
r = random.uniform(size=nsocs)
# in AWS paper: 1e12 (alternatively: 1e13):
S0 = 1e12 * D.gigajoules * r / r.mean()
M.Society.renewable_energy_knowledge.set_values(societies, S0)
# print(M.Society.renewable_energy_knowledge.get_values(societies))

# TODO: add noise to parameters

w = worlds[0]
s = societies[0]
c = cells[0]
for v in nature.variables: print(v,v.get_value(nature))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))

# from pycopancore.private._expressions import eval
# import pycopancore.model_components.base.interface as B
# import sympy as sp

runner = Runner(model=model)

start = time()
traj = runner.run(t_0=2000, t_1=2000+100, dt=1, add_to_output=[M.Individual.represented_population])


for v in nature.variables: print(v,v.get_value(nature))
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
dump(tosave, open("/home/jobst/work/without.pickle","wb"))
print(time()-start, " seconds")

t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

figure()
lws = 1

subplot(511)  # cultural
for i, s in enumerate(societies):
#    plot(t[3:], traj[M.Society.protected_terrestrial_carbon_share][s][3:],color="green",lw=lws, label=None if i else "share of protected biomass")
    plot(t[3:], traj[M.Society.has_renewable_subsidy][s][3:]*1,color="darkorange",lw=lws, label=None if i else "renewable subsidy in place?")
    plot(t[3:], traj[M.Society.has_emissions_tax][s][3:]*1,color="blue",lw=lws, label=None if i else "emissions tax in place?")
    plot(t[3:], traj[M.Society.has_fossil_ban][s][3:]*1,color="gray",lw=lws, label=None if i else "fossil ban in place?")
legend()

subplot(512)  # metabolic, logscale: capital, knowledge, production, wellbeing
for i, s in enumerate(societies):
    semilogy(t[3:], array(traj[M.Society.physical_capital][s][3:])/1e6, color="black", lw=lws, label=None if i else "physical capital [mio. $]")
    semilogy(t[3:], array(traj[M.Society.renewable_energy_knowledge][s][3:])/1e6, color="darkorange", lw=lws, label=None if i else "renewable energy knowledge [PJ]")
    semilogy(t[3:], array(traj[M.Society.economic_output_flow][s][3:])/1e6, color="blue", lw=lws, label=None if i else "GDP [mio. $ per year]")
    semilogy(t[3:], array(traj[M.Society.wellbeing][s][3:]), color="magenta",lw=lws, label=None if i else "wellbeing [$ per year and person]")
legend()

subplot(513)  # metabolic: population (left), migration (right)
ax1 = gca()
#ax1.set_xlabel('years')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('humans')
ax1.tick_params('y')
ax2 = ax1.twinx()
ax2.set_ylabel('humans per year', color='gray')
ax2.tick_params('y', colors='gray')
for i, s in enumerate(societies):
    ax1.plot(t[3:], traj[M.Society.population][s][3:],color="black",lw=lws, label=None if i else "population")
    ax1.plot(t[3:], traj[M.Society.migrant_population][s][3:],"-.",color="black",lw=lws, label=None if i else "migrant population")
    ax2.plot(t[3:], traj[M.Society.immigration][s][3:],"--",color="gray",lw=lws, label=None if i else "immigration flow")
    ax2.plot(t[3:], traj[M.Society.emigration][s][3:],":",color="gray",lw=lws, label=None if i else "emigration flow")
ax1.legend(loc=2)
ax2.legend(loc=1)

subplot(514)  # metabolic: energy mix
for i, s in enumerate(societies):
    Es = array(traj[M.Society.secondary_energy_flow][s][3:])
    plot(t[3:], array(traj[M.Society.biomass_input_flow][s][3:]) * metabolism.biomass_energy_density / Es, color="green", lw=lws, label=None if i else "share of biomass")
    plot(t[3:], array(traj[M.Society.fossil_fuel_input_flow][s][3:]) * metabolism.fossil_energy_density / Es, color="gray", lw=lws, label=None if i else "share of fossils")
    plot(t[3:], array(traj[M.Society.renewable_energy_input_flow][s][3:]) / Es, color="darkorange", lw=lws, label=None if i else "share of renewables")
legend()

subplot(515)  # natural
plot(t[3:], traj[M.World.atmospheric_carbon][worlds[0]][3:], color="cyan", lw=3, label="atmospheric carbon")
plot(t[3:], traj[M.World.upper_ocean_carbon][worlds[0]][3:], color="blue", lw=3, label="upper ocean carbon")
plot(t[3:], traj[M.World.terrestrial_carbon][worlds[0]][3:], color="green", lw=3, label="terrestrial carbon")
plot(t[3:], traj[M.World.fossil_carbon][worlds[0]][3:], color="gray", lw=3, label="fossil carbon")
for i, s in enumerate(societies):
    plot(t[3:], traj[M.Society.protected_terrestrial_carbon][s][3:],color="green",lw=lws, label=None if i else "protected biomass")
gca().set_ylabel('gigatonnes carbon')
legend()

print("\nyr 2000 values (real):")
print("emigration (5e6):",sum(traj[M.Society.emigration][s][5] for s in societies)) # should be ca. 5e6
print("photo (123):",sum(traj[M.Cell.photosynthesis_carbon_flow][c][5] for c in cells))
print("resp (118):",sum(traj[M.Cell.terrestrial_respiration_carbon_flow][c][5] for c in cells))
print("GWP (4e13):",sum(traj[M.Society.economic_output_flow][s][5] for s in societies)) # should be ca. 4e13
Bglobal = sum(traj[M.Society.biomass_input_flow][s][5] for s in societies) * D.gigatonnes_carbon / D.years
Fglobal = sum(traj[M.Society.fossil_fuel_input_flow][s][5] for s in societies) * D.gigatonnes_carbon / D.years
Rglobal = sum(traj[M.Society.renewable_energy_input_flow][s][5] for s in societies) * D.gigajoules / D.years
print("B (3), F (11), R(100):",
      Bglobal.tostr(unit=D.gigatonnes_carbon/D.years), # should be ca. 3
      Fglobal.tostr(unit=D.gigatonnes_carbon/D.years), # should be ca. 11
      Rglobal.tostr(unit=D.gigawatts)) # last should be ca. 100
#print((Bglobal * metabolism.biomass_energy_density * D.gigajoules/D.gigatonnes_carbon).tostr(unit=D.gigawatts),
#      (Fglobal * metabolism.fossil_energy_density * D.gigajoules/D.gigatonnes_carbon).tostr(unit=D.gigawatts),
#      Rglobal.tostr(unit=D.gigawatts), "(100)") # last should be ca. 100
print("life exp. at end:",1/np.mean([traj[M.Society.mortality][s][-1] for s in societies]))
print("cap. deprec. at begin (0.1?):",np.mean([traj[M.Society.physical_capital_depreciation_rate][s][5] for s in societies]))
print("cap. deprec. at end (0.1?):",np.mean([traj[M.Society.physical_capital_depreciation_rate][s][-1] for s in societies]))
print("deaths at begin (>250000?):",sum(traj[M.Society.deaths][s][5] for s in societies))
print("deaths at end (>250000?):",sum(traj[M.Society.deaths][s][-1] for s in societies))
print("temp. at begin:",traj[M.World.surface_air_temperature][worlds[0]][5])
print("temp. at end:",traj[M.World.surface_air_temperature][worlds[0]][-1])
print("prot. carbon share:",[traj[M.Society.protected_terrestrial_carbon][s][-1]/sum(traj[M.Cell.terrestrial_carbon][c][-1]for c in s.cells) for s in societies])
print(traj[M.World.terrestrial_carbon][worlds[0]][-1],sum(traj[M.Cell.terrestrial_carbon][c][-1] for c in worlds[0].cells))

show()

# TODO: 
# policy shares, env. friendly shares
# transparancy, means
# wellb. abs., renew., pop. log
# total protected
# horiz.
# save dump with codename,uid as key