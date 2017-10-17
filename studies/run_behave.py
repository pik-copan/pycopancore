"""Skript to run Jobsts model."""

from time import time
import datetime as dt
# import networkx as nx
import numpy as np
# import sys
# BEHAVE MODEL DOES NOT EXIST YET!
import pycopancore.models.behave as M
# import pycopancore.models.only_copan_global_like_carbon_cycle as M
# from pycopancore import master_data_model as D
from pycopancore.runners import Runner

# import plotly.plotly as py
import plotly.offline as py
import plotly.graph_objs as go

# first thing: set seed so that each execution must return same thing:
np.random.seed(1)
# TODO: figure out why it doesn't seem to work here ...

# parameters:
timeinterval = 100
timestep = 0.1

model_parameters = {}

# TODO: RENAME HERE AND IN CULTURE!
model_parameters['n_individuals'] = 10
model_parameters['mean_degree_pref'] = 10
model_parameters['std_degree_pref'] = 3
model_parameters['interaction_offset'] = 0.03
model_parameters['p_ai'] = 0.8
model_parameters['char_weight'] = [0.2, 0.8]
model_parameters['p_rew'] = 0.03


degree_preference = [np.random.normal(loc=10.0, scale=3.0)
                     for _ in range(model_parameters['n_individuals'])]



# instantiate model
model = M.Model()

def distribution_function(yb, x):
    """"
    Modulate the parabolic distribution y= a(b-x)**2 +c fct. with the
    following boundary conditions:
      - 1. x=0: y == 3 : follows from the initial distribution function
      - 2. Int[0,1] == 1: normalization criteria
      - 3. x=1: y == yb, where yb is the tunable parameter, which reflects
          the probability for an agent to have smoking disposition 1
        yb0==3
    """
    # print('yb', yb)
    # yb = 3
    b = (1. + yb / 3) / (1 + yb)
    a = 2. / (b - 1. / 3)
    c = 3. - a * b ** 2

    return a * (b - x) ** 2 + c


def rejection_sampling(N, distribution_function_ini, yb):
    """
    Creates random sampling of an arbitrary distribution using the rejection
    sampling method for a continuous characteristic (e.g. smoking disposition)
    and a second binary characteristic based on this.
    """
    result = np.zeros((2, N))

    i = 0
    while i < N:
        random_numbers = np.random.random(2)
        if 3.0 * random_numbers[0] < distribution_function_ini(yb,
                                                         random_numbers[1]):
            result[0, i] = random_numbers[1]
            # if the smoking disposition is greater than a certain value,
            # the binary characteristic smoker/non-smoker is assigned
            result[1, i] = int(random_numbers[1] > .5)
            i += 1

    return result[0, :], result[1, :]

# TODO: BEHAVIOR SHOULD BE INT ARRAY!!
initial_disposition, initial_behavior = rejection_sampling(model_parameters['n_individuals'],
                                                           distribution_function, 3.0)


# TODO: SHIT! INDIVIDUALS ARE NOT YET IN CULTURE WHEN CULTURE IS INSTANTIATED, GET DEGREE PREFERENCE IN CULTURE METHOD.
# instantiate process taxa:
culture = M.Culture(model_parameters = model_parameters)

# generate entities and distribute opinions uniformly randomly:
world = M.World(culture=culture)
cell = M.Cell(world=world)
# TO BE CHANGED!
individuals = [M.Individual(initial_disposition = initial_disposition[i],
                            degree_preference = np.random.normal(loc = model_parameters['mean_degree_pref'],
                                                                 scale = model_parameters['std_degree_pref']),
                            initial_behavior = initial_behavior[i],
                            cell = cell
                            )
               for i in range(model_parameters['n_individuals'])]


def erdosrenyify(graph, p=0.5):
    """Create a ErdosRenzi graph from networkx graph.

    Take a a networkx.Graph with nodes and distribute the edges following the
    erdos-renyi graph procedure.
    """
    assert not graph.edges(), "your graph has already edges"
    nodes = graph.nodes()
    for i, n1 in enumerate(nodes[:-1]):
        for n2 in nodes[i+1:]:
            if np.random.random() < p:
                graph.add_edge(n1, n2)

#print(len(individuals))
#print(individuals[0].instances)
#print(individuals[0].get_instances())

# # set the initial graph structure to be an erdos-renyi graph
# print("erdosrenyifying the graph ... ", end="", flush=True)
# start = time()
# erdosrenyify(culture.acquaintance_network, p=expected_degree / nindividuals)
# print("done ({})".format(dt.timedelta(seconds=(time() - start))))
#
# runner = Runner(model=model)
#
# start = time()
# traj = runner.run(t_1=timeinterval, dt=timestep)
# runtime = dt.timedelta(seconds=(time() - start))
# print("runtime: {runtime}".format(**locals()))
#
#
# t = np.array(traj['t'])
# print("max. time step", (t[1:]-t[:-1]).max())
#
# individuals_opinions = np.array([traj[M.Individual.opinion][ind]
#                                  for ind in individuals])
#
# nopinion1_list = np.sum(individuals_opinions, axis=0) / nindividuals
# nopinion0_list = 1 - nopinion1_list
#
# # everything below is just plotting commands for plotly
#
# data_opinion0 = go.Scatter(
#     x=t,
#     y=nopinion0_list,
#     mode="lines",
#     name="relative amount opinion 0",
#     line=dict(
#         color="lightblue",
#         width=2
#     )
# )
# data_opinion1 = go.Scatter(
#     x=t,
#     y=nopinion1_list,
#     mode="lines",
#     name="relative amount opinion 1",
#     line=dict(
#         color="orange",
#         width=2
#     )
# )
# data_majority_opinion = go.Scatter(
#     x=t,
#     y=traj[M.Society.opinion][society],
#     mode="lines+markers",
#     name="majority opinion",
#     line=dict(
#         color="red",
#         width=2
#     ),
#     marker=dict(
#         color="red",
#         size=4
#     )
# )
#
# layout = dict(title='Adaptive Voter Model',
#               xaxis=dict(title='time'),
#               )
#
# fig = dict(data=[data_opinion0, data_opinion1, data_majority_opinion], layout=layout)
# py.plot(fig, filename="adaptive-voter-model.html")
