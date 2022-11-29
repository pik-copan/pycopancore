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

#import os

# os.chdir('C:/Users/hhpra/Desktop/Ausbildung/Hu_Berlin/INRM/Masterarbeit/CopanCore/pycopancore-master')

from pycopancore.models import BBC_2

# standard runner for simulating any model:
from pycopancore.runners.runner import Runner

# from pycopancore import master_data_model as D  # to be able to specify variables with physical units

import numpy as np  # which is usually needed
# from numpy.random import choice, uniform  # to generate random initial conditions

import pylab as plt  # to plot stuff

# instantiate the model and have it analyse its own structure:
model = BBC_2.Model()
environment = BBC_2.Environment

#
# TODO: All necessary model setup, such as setting initial conditions or
# instantiating taxa and entities, comes after this line and before the next
# commented block below. The following code is exemplary:
#


# model parameters:

# nsocs = 2  # no. of social systems
# ncellseach = 10  # no. of cells per social system
# nindseach = 10  # no. of individuals per cell
# link_density = 0.1  # random network link density

# simulation parameters:
# Environment Parameter


# Culture Parameter
# beta_BD = 0.005
# gamma_BD = 0.5
# Ef_BD = 1
# e_A_BD = 1
# e_SN_BD = 1
# e_PBC_BD = 1
# SN_BD = 1
# PBC_BD = 1

# alpha = 0.66

# beta_CC = 0.005
# gamma_CC = 0.5
# Ef_CC = 1
# e_A_CC = 1
# e_SN_CC = 1
# e_PBC_CC = 1
# SN_CC = 1
# PBC_CC = 1

# Metabolism Parameter
# E_min_BD = 0.01
# R_max_BD = 1

# E_min_CC = 20
# R_max_BD = 1


# simulation parameters
t_max = 1900  # interval for which the model will be simulated
dt = 1  # desired temporal resolution of the resulting output.

# instantiate process taxa:
env = BBC_2.Environment(
    response_lag=0,
    #measurre_biodiv=0.9,
    #productivity=0.973,
    bio_pump_strength=13,
    perma_carbon=0,
    perma_tenperature=0,
    temperature=0,
    carbon_atmosphere=589,
    carbon_terrestial=1875,
    terrestrial_carbon_cap=1687.5,
    #carbon_ocean=900,
    carbon_mixed_laxer=900,
    partial_pressure=589,
    carbon_system=0,
    K_c=0.3,
    c_a0=589,
    c_t0=1875,
    c_m0=900,
    K_A=55,
    NPP=55,
    Q_R=1.72,
    tau=4,
    lam=1.8,
    I_CC=0.05,
    teta=0.26,
    v_max=0.02,
    r_g=0.025,
    p_T=22.5,
    Dd=1,
    r=12.5,
    D_T=0.0423,
    B_0=13,
    B_T=0.032,
    B_TB=0.007,
    B_A=0.019,
    w_0=0.1,
    w_T=0.1,
    LUC=1,
    I_d=0.1,
    e=10,
    dis=0
    # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
)
# met = M.Metabolism(
#    # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
#    )
# cul = M.Culture(
#    # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
#    )

# generate entities:
# world = M.World(
#            environment = env,
#            metabolism = met,
#            culture = cul,
#            # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
#            )  # TODO: in case of many worlds, make a list
# socs = [M.SocialSystem(world = world,
#            # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
#            ) for j in range(nsocs)]
# cells = [M.Cell(social_system = s,
#            # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
#            ) for s in socs for j in range(ncellseach)]
# inds = [M.Individual(cell = c,
#            # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
#            ) for c in cells for j in range(nindseach)]

# set some further variables:
# P0 = uniform(high=1e3, size=nsocs)
# M.SocialSystem.population.set_values(socs, P0)

# initialize some network:
# for index, i in enumerate(inds):
#    for j in inds[:index]:
#        if uniform() < link_density:
#            cul.acquaintance_network.add_edge(i, j)

#
# Run the model
#

runner = Runner(model=model)
traj = runner.run(t_0=1800, t_1=t_max, dt=dt)

# TODO: Add some further analysis such as plotting or saving
#Biodiversity = traj[BBC_2.Environment.measurre_biodiv]
#Temperature = traj[BBC_2.Environment.temperature]
#print(Temperature[0])
#plt.plot(traj['t'], Biodiversity, 'g', label="Biodiversity loss")
#plt.plot(traj['t'], Temperature, 'b', label="Global mean temperature")
#plt.show()

t = np.array(traj['t'])
temp =list(traj[BBC_2.Environment.temperature].values())
temp_1 = (temp[0])
plt.plot(traj['t'], temp_1)
#carb_at = list(traj[BBC_2.Environment.carbon_atmosphere].values())
#carb_at_1 = (carb_at[0])
#plt.plot(traj['t'], carb_at_1)
#carb_mi = list(traj[BBC_2.Environment.carbon_mixed_laxer].values())
#carb_mi_1 = (carb_mi[0])
#plt.plot(traj['t'], carb_mi_1)
#carb_te = list(traj[BBC_2.Environment.carbon_terrestial].values())
#carb_te_1 = (carb_te[0])
#plt.plot(traj['t'], carb_te_1)
#resp = list(traj[BBC_2.Environment.response_lag].values())
#resp_1 = (resp[0])
#plt.plot(traj['t'], resp_1)
plt.show()