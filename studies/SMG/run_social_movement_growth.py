"""Run script for the Social Movement Growth model by Leander John."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

import os
import sys
# Set the path for importing modules (assuming this file resides in a
# subfolder of the "studies" folder, meaning going two folders up):
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dataclasses import dataclass

import pycopancore.models.social_movement_growth as M

# Standard runner for simulating any model:
from pycopancore.runners.runner import Runner

# To be able to specify variables with physical units:
from pycopancore import master_data_model as D

import numpy as np  # which is usually needed
# To generate random initial conditions:
from numpy.random import default_rng

import networkx as nx
import pickle
import yaml
import time

rng = default_rng()

# Model parameters:
@dataclass
class Parameters:
    growth_strategy: float = .9
    
    meeting_rate: float = 12 # per year
    interaction_rate: float = 52 # per year
    
    mobilizing_success_probability: float = .2
    organizing_success_probability: float = .1
    
    ninds: int = 500
    ninds_core: int = 1
    ninds_base: int = 0
    ninds_support: int = 0
    ninds_indifferent: int = ninds - ninds_core - ninds_base - ninds_support
    
    network: str = "BA"
    mean_degree: int = 20 # will be floored to even for BA network.
    
    # Simulation parameters:
    t_max: float = 5. # interval for which the model will be simulated.
    dt: float = .1 # desired temporal resolution of the resulting output.

p = Parameters()


# Instantiate the model and have it analyse its own structure:
model = M.Model()

# Instantiate process taxa:
env = M.Environment()
met = M.Metabolism()
cul = M.Culture(
    growth_strategy = p.growth_strategy,
    meeting_rate = p.meeting_rate,
    interaction_rate = p.interaction_rate,
    mobilizing_success_probability = p.mobilizing_success_probability,
    organizing_success_probability = p.organizing_success_probability
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
    ) for j in range(p.ninds_core)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'base'
    ) for j in range(p.ninds_base)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'support'
    ) for j in range(p.ninds_support)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'indifferent'
    ) for j in range(p.ninds_indifferent)]

# Shuffle for later network initialization:
rng.shuffle(inds)

# Initialize network:
print("Initializing network …")
if p.network == "BA":
    # Initialize Barabasi-Albert network:
    N = p.ninds
    m0 = p.mean_degree//2 # size of the initial (fully connected) clique
    m = p.mean_degree//2 # number of connections for each new node
    edges = []

    # Add the edges of the initial clique connecting all the m nodes:
    for i in range(m0):
        for j in range(i+1, m0):
            edges.append((inds[i], inds[j]))

    # Run over all the remaining nodes:
    prob = [node for edge in edges for node in edge]
    for i in range(m0, N):
        # For each new node, create m new links:
        target_nodes = rng.choice(prob, m)
        edges.extend(list(zip([inds[i]] * m, target_nodes)))
        
        # update prob list
        prob.extend(target_nodes)
        prob.extend([inds[i]] * m)

    cul.acquaintance_network.add_edges_from(edges)
print("Network initialization complete.")

#
# Run the model:
#

runner = Runner(model=model)
traj = runner.run(t_0=0, t_1=p.t_max, dt=p.dt,
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
# ATTENTION this only saves the network at t=0 since as of now the
# network is constant and saving for each TP is computationally
# intensive
tosave["Culture.acquaintance_network"] = {
    str(e): 
        [(str(a), str(b), c) for (a,b,c) in nx.to_edgelist(
            traj[M.Culture.acquaintance_network][e][0]
            )]
    for e in traj[M.Culture.acquaintance_network].keys()
    }
tosave["t"] = traj["t"]

# Define directory and file name for config and results to be saved:
res_dir = "./simulation_results/SMG/"
date_str = time.strftime("%Y-%m-%d/")
time_str = time.strftime("%H%M%S")
filename = res_dir+date_str+time_str
if not os.path.exists(res_dir+date_str):
    os.makedirs(res_dir+date_str)

# Save configuration parameters:
with open(filename+"_conf.yaml", "w") as f:
    yaml.safe_dump(p, f, sort_keys=False)

# Save trajectory results:
with open(filename+".pickle", "wb") as f:
    pickle.dump(tosave, f)

# Add the date and time to the log file:
with open(res_dir+"all_runs.txt", "a") as f:
    f.write(date_str+time_str+"\n")
