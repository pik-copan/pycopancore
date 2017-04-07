"""Skript to run Jobsts model."""

from time import time
# from numpy import random
import random
import numpy as np
import pycopancore.models.adaptive_voter_model as M
# import pycopancore.models.only_copan_global_like_carbon_cycle as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

# import plotly.plotly as py
import plotly.offline as py
import plotly.graph_objs as go
# from pylab import plot, gca, show

# assert False, "to be changed"

# first thing: set seed so that each execution must return same thing:
random.seed(1)

# parameters:

# nworlds = 1  # no. worlds
# nsocs = 1  # no. societies
# ncells = 1  # no. cells
nindividuals = 100
rewiring_probability = 0.1
possible_opinions = list(range(2))

model = M.Model()

# instantiate process taxa:
# nature = M.Nature()
culture = M.Culture(rewiring_probability=rewiring_probability)
# metabolism = M.Metabolism()

# generate entities and plug them together at random:
world = M.World(culture=culture)
cell = M.Cell(world=world)
# worlds = [M.World(nature=nature, #metabolism=metabolism,
#                   atmospheric_carbon=830 * D.gigatonnes_carbon,
#                   ocean_carbon=(5500 - 830 - 2480 - 1125) * D.gigatonnes_carbon
#                   ) for w in range(nworlds)]
# societies = [M.Society(world=random.choice(worlds)) for s in range(nsocs)]
# cells = [M.Cell(society=random.choice(societies)) for c in range(ncells)]
individuals = [M.Individual(cell=cell, initial_opinion=random.choice(possible_opinions))]


runner = Runner(model=model)

start = time()
traj = runner.run(t_1=100, dt=.1)
print(time()-start, " seconds")

assert False, "ignore rest for now, will make proper plots with plotly when the above is running"

t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

data_ca = go.Scatter(
    x=t,
    y=traj[M.World.atmospheric_carbon][worlds[0]],
    mode="lines",
    name="atmospheric carbon",
    line=dict(
        color="lightblue",
        width=4
    )
)
data_ct = go.Scatter(
    x=t,
    y=traj[M.World.terrestrial_carbon][worlds[0]],
    mode="lines",
    name="terrestrial carbon",
    line=dict(
        color="green",
        width=4
    )
)
data_cm = go.Scatter(
    x=t,
    y=traj[M.World.ocean_carbon][worlds[0]],
    mode="lines",
    name="maritime carbon",
    line=dict(
        color="blue",
        width=4
    )
)
data_cf = go.Scatter(
    x=t,
    y=traj[M.World.fossil_carbon][worlds[0]],
    mode="lines",
    name="fossil carbon",
    line=dict(
        color="gray",
        width=4
    )
)
layout = dict(title = 'Our model (simple Carbon Cycle for now)',
              xaxis = dict(title = 'time [yr]'),
              yaxis = dict(title = 'Carbon [GtC]'),
              )

fig = dict(data=[data_ca, data_ct, data_cm, data_cf], layout=layout)
py.plot(fig, filename="our-model-result.html")

for s in societies:
    pass
## the stuff below is still matplotlib style, needs to be converted to plotly
#    plot(t, traj[M.Society.population][s],"yellow",lw=2)
#     plot(t, traj[M.Society.physical_capital][s], "k", lw=2)
#     plot(t, traj[M.Society.renewable_energy_knowledge][s],
#          color="darkorange", lw=2)
#     plot(t, traj[M.Society.biomass_input_flow][s], "g--", lw=2)
#     plot(t, traj[M.Society.fossil_fuel_input_flow][s],
#          "--", color="gray", lw=2)
#     plot(t, traj[M.Society.renewable_energy_input_flow][s],
#          "--", color="darkorange", lw=2)
for c in cells:
    pass
#    plot(t, traj[M.Cell.terrestrial_carbon][c],"g")
#    plot(t, traj[M.Cell.fossil_carbon][c],"gray")
# gca().set_yscale('symlog')
# show()
