#
# TODO:
# 
# Either Import a model from pycopancore ...
from pycopancore.models import MODEL as M

# ... or import a model you designed yourself
import model as M 

# You need a runner to run your model. Do not remove this.
from pycopancore.runners.runner import Runner

#
# Initiate the model. This is required. Do not remove this line.
#
model = M.Model()

#
# TODO: All necessary model setup, such as setting initial conditions or
# instantiating taxa and entities, comes here
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

#
# TODO: Add some further analysis such as plotting or saving
#
time = traj["t"]  # For example
