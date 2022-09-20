"""Run script for the Social Movement Growth model by Leander John."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# Set the path for importing modules (assuming this file resides in a
# subfolder of the "studies" folder):
from os.path import dirname
import sys
sys.path.insert(0, dirname(dirname(dirname(__file__))))

import pycopancore.models.social_movement_growth as M

# Standard runner for simulating any model:
from pycopancore.runners.runner import Runner

# To be able to specify variables with physical units:
from pycopancore import master_data_model as D

import numpy as np  # which is usually needed
# To generate random initial conditions:
from numpy.random import choice, uniform
import random

import networkx as nx
from pickle import dump

filename = "/tmp/smg_data.p"

# Model parameters:
growth_strategy = 0.2
meeting_rate = 2 / D.months
organizing_success_probability = 0.2
mobilizing_success_probability = 0.2

ninds_core = 5
ninds_base = 10
ninds_support = 50
ninds_inactive = 150

ninds = ninds_core + ninds_base + ninds_support + ninds_inactive

# Simulation parameters:
t_max = 5  # interval for which the model will be simulated
dt = 0.1  # desired temporal resolution of the resulting output.


# Instantiate the model and have it analyse its own structure:
model = M.Model()

# Instantiate process taxa:
env = M.Environment()
met = M.Metabolism()
cul = M.Culture(
    growth_strategy = growth_strategy,
    meeting_rate = meeting_rate,
    organizing_success_probability = organizing_success_probability,
    mobilizing_success_probability = mobilizing_success_probability,
    )

# Generate entities:
world = M.World(
    environment = env,
    metabolism = met,
    culture = cul,
    )
soc = M.SocialSystem(
    world = world,
    )
cell = M.Cell(
    social_system = soc,
    )
inds = [M.Individual(
    cell = cell,
    engagement_level = 'core'
    ) for j in range(ninds_core)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'base'
    ) for j in range(ninds_base)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'support'
    ) for j in range(ninds_support)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'inactive'
    ) for j in range(ninds_inactive)]

# Shuffle for later network initialization:
random.shuffle(inds)

# Set some further variables:

# Initialize Barabasi-Albert network:
N = ninds
m0 = 3 # size of the initial (fully connected) clique
m = 3 # number of connections for each new node
edges = []

# Add the edges of the initial clique connecting all the m nodes:
for i in range(m0):
    for j in range(i+1, m0):
        edges.append((inds[i], inds[j]))

# Run over all the remaining nodes:
for i in range(m0, N):
    # Flatten the edges array so each node appears proportional to the
    # number of links it has:
    prob = [node for edge in edges for node in edge]
    # For each new node, create m new links:
    for j in range(m):
        # Pick up a random node, so nodes will be selected
        # proportionally to their degree:
        node = choice(prob)
        edges.append((inds[i], node))

cul.acquaintance_network.add_edges_from(edges)


#
# Run the model:
#

runner = Runner(model=model)
traj = runner.run(t_0=0, t_1=t_max, dt=dt,
                  add_to_output=[M.Individual.engagement_level, 
                                 M.Culture.acquaintance_network]
                  )

# Create a dictionary of variable trajectories to pickle:
# ATTENTION str(<Culture object>) does not work as expected.
tosave = {
          v.owning_class.__name__ + "."
          + v.codename: {str(e): traj[v][e]
                         for e in traj[v].keys()
                         } 
          for v in traj.keys() if v != "t"
          }
# Need to overwrite graph objects due to an error with pickling
# Individual type as nodes. TODO Check problem with DUMMY variable
tosave["Culture.acquaintance_network"] = {
    str(e): [[(str(a), str(b), c) for (a,b,c) in nx.to_edgelist(tp)]
             for tp in traj[M.Culture.acquaintance_network][e]]
    for e in traj[M.Culture.acquaintance_network].keys()
    }

tosave["t"] = traj["t"]

dump(tosave, open(filename, "wb"))
#dump(cul.acquaintance_network, open("/tmp/network.p", "wb"))
