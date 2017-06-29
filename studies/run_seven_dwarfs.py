"""This is the test script for the seven dwarfs step by step tutorial.

In this version only the Step-process 'aging' of entitytype 'Individual' is
implemented, such that the only relevant attributes of 'Individual' are 'age'
and 'cell'.
"""

import numpy as np
from time import time
import datetime as dt

import plotly.offline as py
import plotly.graph_objs as go

import pycopancore.models.seven_dwarfs as M
from pycopancore.runners.runner import Runner


# setting timeinterval for run method 'Runner.run()'
timeinterval = 100
# setting time step to hand to 'Runner.run()'
timestep = 1
nc = 1  # number of caves
dwarfs = 7  # number of dwarfs

# instantiate model M (needs to be done in the beginning of each script).
# This configures the model M through 'ModelLogics' in module
# 'base.model_logics' such that initialisation of attributes and entities gets
# possible
model = M.Model()

# instantiate process taxa culture:
# In this certain case we need 'M.Culture()' for the acquaintance network.
culture = M.Culture()

# instantiate world:
world = M.World(culture=culture)

# instantiate cells (the caves)
cell = [M.Cell(world=world,
#                stock=100
               )
         for c in range(nc)
        ]

# instantiate dwarfs and assigning initial conditions
individuals = [M.Individual(cell=cell[0],
                            age=0,
#                            beard_length=0,
#                            beard_growth_parameter=0.1,
#                            eating_parameter=1
                            ) for i in range(dwarfs)
               ]

# assigning individuals to cell is not necessary since it is done by
# initializing the individuals in 'base.Individuals' with the 'cell' method


start = time()

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

# saving time values to t
t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())


# proceeding for plotting


individuals_age = np.array([traj[M.Individual.age][dwarf]
                                 for dwarf in individuals])


t = np.array(traj['t'])

data_age = []
print('data age', data_age)
for i in range(dwarfs):
    data_age.append(object)
    data_age[i] = go.Scatter(
        x=t,
        y=individuals_age[i],
        mode="lines",
        name="age of dwarf no. {}".format(i),
        line=dict(
            color="green",
            width=4
        )
    )



layout = dict(title = 'seven dwarfs',
              xaxis = dict(title = 'time [yr]'),
              yaxis = dict(title = 'age'),
              )


# getting plots of two dwarfs
fig1 = dict(data=[data_age[0]], layout=layout)
py.plot(fig1, filename="our-model-result1.html")

fig2 = dict(data=[data_age[1]], layout=layout)
py.plot(fig2, filename="our-model-result2.html")