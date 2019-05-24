"""
Run script template.

TODO: Go through the file and adjust all parts of the code marked with the TODO
flag. Pay attention to those variables and objects written in capital letters.
These are placeholders and must be adjusted as needed. For further details see
also the model development tutorial.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
 
# TODO: (uncomment if needed) Import a model from pycopancore ...
# import pycopancore.models.SOMEMODEL as M 

# You need a runner to run your model. Do not remove this.
from pycopancore.runners.runner import Runner

#
# Initiate the model. This is required. Do not remove this line.
#
model = M.Model()

#
# TODO: All necessary model setup, such as setting initial conditions or
# instantiating taxa and entities, comes after this line and before the next
# commented block below
#

#
# Run the model
#
# The interval for which the model will be integrated forward, adjust as
# needed
TIMEINTERVAL = 50    

# The temporal resolution of the resulting trajectory. Increase to save
# memory
TIMESTEP = 0.1

runner = Runner(model=model)
traj = runner.run(t_1=TIMEINTERVAL, dt=TIMESTEP)

# TODO: Add some further analysis such as plotting or saving
time = traj["t"]  # For example
