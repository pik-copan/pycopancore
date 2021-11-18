"""Skript to run Jobsts prototype model."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from time import time
from numpy import random, array
import numpy as np
import pycopancore.models.only_granovetter as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show, figure, subplot, gca, semilogy, legend

# first thing: set seed so that each execution must return same thing:
random.seed(10) # 10

# parameters:

nworlds = 1  # no. worlds
nsocs = 5 # no. social_systems #10
ncells = 100  # no. cells #100
ninds = 1000 # no. individuals

t_1 = 2050

filename = "/tmp/granvegano.pickle"

model = M.Model()

is_active = [random.choice([False, True], p=[.8, .2]) for i in range(ninds)]

# instantiate process taxa:
environment = M.Environment()
metabolism = M.Metabolism()
culture = M.Culture(
                    number_of_active_individuals = len(is_active)
                    )

# generate entities and plug them together at random:
worlds = [M.World(environment=environment, metabolism=metabolism, culture=culture
                  ) for w in range(nworlds)]
social_systems = [M.SocialSystem(world=random.choice(worlds)
                       ) for s in range(nsocs)]
cells = [M.Cell(social_system=random.choice(social_systems)
         ) for c in range(ncells)]
individuals = [M.Individual(
                cell=random.choice(cells),
                is_active = 
                    random.choice([False, True], p=[.8, .2]), #True, #False,
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
                else p_samesoc if i.social_system == j.social_system \
                else p_other):
            culture.acquaintance_network.add_edge(i, j)
#print("degrees:",culture.acquaintance_network.degree())

# TODO: add noise to parameters

w = worlds[0]
s = social_systems[0]
c = cells[0]
i = individuals[0]
for v in environment.variables: print(v,v.get_value(environment))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in culture.variables: print(v,v.get_value(culture))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))
for v in i.variables: print(v,v.get_value(i))

# from pycopancore.private._expressions import eval
# import pycopancore.model_components.base.interface as B
# import sympy as sp

runner = Runner(model=model)

start = time()
traj = runner.run(t_0=2000, t_1=t_1, dt=1, 
                  add_to_output=[M.Culture.number_of_active_individuals]
                  )


for v in environment.variables: print(v,v.get_value(environment))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in culture.variables: print(v,v.get_value(culture))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))
for v in i.variables: print(v,v.get_value(i))


from pickle import dump
tosave = {
          v.owning_class.__name__ + "."
          + v.codename: {str(e): traj[v][e]
                         for e in traj[v].keys()
                         } 
          for v in traj.keys() if v is not "t"
          }
tosave["t"] = traj["t"]
if True: # was only used for debugging:
    for k,v in tosave.items():
        print(k, type(k), type(v))
        assert type(k) ==  type("") and type(v) in [type([]), type({})]
        if type(v) == type({}):
            for k2,v2 in v.items():
                assert type(k2) ==  type("") and type(v2) in [type([]), type({})]
                print(" ", k2, type(k), type(v2))
                if type(v2) == type([]) and len(v2)>0:
                    print("  ", v2[0], type(v2[0])) 
                    for i in v2:
                        assert type(i) in [type(1.0), type(1), type(True), np.int64, np.bool_, np.float64], str(type(i))
dump(tosave, open(filename,"wb"))
print(time()-start, " seconds")

t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

