# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

import numpy as np
from time import time
import datetime as dt

import someplotlibrary as plt

import pycopancore.models.x as M
from pycopancore.runners.runner import Runner

# Set parameters
#parameter1 = 2.5
#parameter2


model = M.Model()

# instantiate process taxa culture:
# In this certain case we need 'M.Culture()' for the acquaintance network.
culture = M.Culture()

# instantiate world:
world = M.World(culture=culture)

# instantiate cells (the caves)
cell = [M.Cell(world=world,
               eating_stock=100
               )
        for c in range(nc)
        ]

# instantiate dwarfs and assigning initial conditions
individuals = [M.Individual(cell=cell[0],
                            age=0,
                            beard_length=0,
                            beard_growth_parameter=0.5,
                            eating_parameter=.1
                            ) for i in range(dwarfs)
               ]

tart = time()

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')

# Define termination signals as list [ signal_method, object_method_works_on ]
# the termination method 'check_for_extinction' must return a boolean
termination_signal = [M.Culture.check_for_extinction,
                      culture]

# Define termination_callables as list of all signals
termination_callables = [termination_signal]


# Runner is instantiated
r = Runner(model=model,
           termination_calls=termination_callables
           )

start = time()
# run the Runner and saving the return dict in traj
traj = r.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))

# Plot routines