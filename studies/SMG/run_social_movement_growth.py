"""Run script for the Social Movement Growth model by Leander John."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# Set the path for importing modules (assuming this file resides in a
# subfolder of the "studies" folder):
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

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
import yaml
import time

# Model parameters:
p = {
    "growth_strategy": 0.8,
    
    "meeting_rate": 12,
    "interaction_rate": 365,
    
    "mobilizing_success_probability": .2,
    "organizing_success_probability": .1,
    
    "ninds": 500,
    "ninds_core": 1,
    "ninds_base": 0,
    "ninds_support": 0,
    
    "network": "BA",

    # Simulation parameters:
    "t_max": 5,  # interval for which the model will be simulated
    "dt": 0.1,  # desired temporal resolution of the resulting output.
}
p["ninds_indifferent"] = p["ninds"] - p["ninds_core"] - p["ninds_base"] - p["ninds_support"]

res_dir = "./simulation_results/social_movement_growth/"
date_str = time.strftime("%Y-%m-%d/")
time_str = time.strftime("%H%M%S")
filename = res_dir+date_str+time_str
if not os.path.exists(res_dir+date_str):
    os.makedirs(res_dir+date_str)

yaml.dump(p, open(filename+"_conf.yaml", "w"), sort_keys=False)
open(res_dir+"last_run.txt", "w").write(date_str+time_str)

# Instantiate the model and have it analyse its own structure:
model = M.Model()

# Instantiate process taxa:
env = M.Environment()
met = M.Metabolism()
cul = M.Culture(
    growth_strategy = p["growth_strategy"],
    meeting_rate = p["meeting_rate"],
    interaction_rate = p["interaction_rate"],
    mobilizing_success_probability = p["mobilizing_success_probability"],
    organizing_success_probability = p["organizing_success_probability"],
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
    ) for j in range(p["ninds_core"])] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'base'
    ) for j in range(p["ninds_base"])] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'support'
    ) for j in range(p["ninds_support"])] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'indifferent'
    ) for j in range(p["ninds_indifferent"])]

# Shuffle for later network initialization:
random.shuffle(inds)

# Set some further variables:

if p["network"] == "BA":
    # Initialize Barabasi-Albert network:
    N = p["ninds"]
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
traj = runner.run(t_0=0, t_1=p["t_max"], dt=p["dt"],
                  add_to_output=[M.Individual.engagement_level, 
                                 M.Culture.acquaintance_network]
                  )


#
# Save the trajectory:
#

# Create a dictionary of variable trajectories to pickle:
# FIXME str(<Culture object>) does not work as expected.
tosave = {
          v.owning_class.__name__ + "."
          + v.codename: {str(e): traj[v][e]
                         for e in traj[v].keys()
                         } 
          for v in traj.keys() if v != "t"
          }
# Need to overwrite graph objects due to an error with pickling
# 'Individual' type as nodes. TODO Check problem with DUMMY variable
# ATTENTION this only saves the network at t=0 as of now the network
# is constant and saving for each TP is computationally intensive
tosave["Culture.acquaintance_network"] = {
    str(e): 
        [(str(a), str(b), c) for (a,b,c) in nx.to_edgelist(
            traj[M.Culture.acquaintance_network][e][0]
            )]
    for e in traj[M.Culture.acquaintance_network].keys()
    }
tosave["t"] = traj["t"]

dump(tosave, open(filename+".pickle", "wb"))
