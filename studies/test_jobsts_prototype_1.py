from random import choice
import pycopancore.models.jobsts_prototype_1 as M
from pycopancore.runners import Runner
from pylab import semilogy, show

# parameters:

nw = 1  # no. worlds
ns = 10  # no. societies
nc = 100  # no. cells

# instantiate process taxa:
nature = M.Nature()
metabolism = M.Metabolism()
# generate entities and plug them together at random:
worlds = [M.World(nature=nature, metabolism=metabolism) for w in range(nw)]
societies = [M.Society(world=choice(worlds)) for s in range(ns)]
cells = [M.Cell(society=choice(societies)) for c in range(nc)]
# make references consistent:
for c in cells:
    c.world = c.society.world

# TODO: add noise to parameters

model = M.Model()

runner = Runner(model=model)

traj = runner.run(t_1=1, dt=0.1)

print(traj['t'], traj[M.World.ocean_carbon][worlds[0]])
semilogy(traj['t'], traj[M.World.ocean_carbon][worlds[0]])
show()
