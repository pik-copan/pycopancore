#
# NEED TO:
# 
# Either Import a model from pycopancore ...
from pycopancore.models import MODEL as M

# ... or import a model you designed yourself
import model as M 

# You need a runner to run your model. Do not remove this.
from pycopancore.runners.runner import Runner

# Initiate the model. This is required. Do not remove this line.
model = M.Model()

#
# NEED TO: Set up the rest of you model, i.e., instantiate instancen, set
# initial consitions
#
#culture = exploit.Culture(linking_probability=0.05, expected_waiting_time=2)
#world = exploit.World(culture=culture)
#
#cells = []
#individuals = []
#
#for _ in range(N):
#    one_cell = exploit.Cell(initial_stock=0.5, growth_rate=1, capacity=1,
#                            world=world)
#    one_individual = exploit.Individual(initial_effort=0.5, trait=0.5,
#                                        cell=one_cell)
#    cells.append(one_cell)
#    individuals.append(one_individual)

# Run the model

# The interval for which the model will be integrated forward, adjust as
# needed
TIMEINTERVAL = 50    

# The temporal resolution of the resulting trajectory. Increase to save
# memory
TIMESTEP = 0.1

runner = Runner(model=model)
traj = runner.run(t_1=TIMEINTERVAL, dt=TIMESTEP)

#
# NEED TO: Add some further analysis such as plotting or saving
#
time = traj["t"]  # For example
