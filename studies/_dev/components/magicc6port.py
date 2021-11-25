"""Script to run magicc6port_only model."""

from time import time
from numpy import random, array
import numpy as np

import pycopancore.models.magicc6port_only as M
import pycopancore.model_components.base as B
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show, figure, subplot, gca, semilogy, legend

from numba.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

# first thing: set seed so that each execution must return same thing:
random.seed(10)

# parameters:

t_1 = 2120

# directory to store results:
filename = "/tmp/";

print("Using model as defined in file", M.__file__)
model = M.Model()
runner = Runner(model=model)

# PARAMETERS:
    
# To do!


# INITIAL VALUES:
    
# initial stocks:
A0 = 1
P0 = 1
H0 = 2
S0 = 3

# initial flows:
L0 = 4
Q0 = 5
U0 = 6

environment = M.Environment ( )

world = M.World (environment=environment,
    carbon_stock_atmospheric_CO2 = A0,
    carbon_stock_living_plants = P0,
    carbon_stock_detritus = H0,
    carbon_stock_soils = S0,
    initial_carbon_flow_litter_production = L0,
    initial_carbon_flow_detritus_decay = Q0,
    initial_carbon_flow_soils_oxidization = U0,
    turnover_time_living_plants = P0 / L0, # (A5) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle
    turnover_time_detritus = H0 / Q0, # (A6) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle
    turnover_time_soils = S0 / U0, # (A7) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle
    )

start = time()
traj = runner.run(t_0=2000, t_1=t_1, dt=1)
print(time()-start, " seconds")


# plotting:

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pycopancore import Variable

# extract time points, entity types/process taxa, variable codenames, instances:
t = np.array(traj['t'])
nts = t.size
etpts = []
codenames = {}
vars = {}
units = {}
colors = {}
instances = {}
for var, value in traj.items():
    if not isinstance(var, Variable): continue
    etpt = var.owning_class.__name__
    codename = var.codename
    if etpt not in etpts:
        ins = list(value.keys())
        if len(ins)>0:
            etpts.append(etpt)
            codenames[etpt] = []
            instances[etpt] = ins
    if etpt in etpts:
        codenames[etpt].append(codename)
        colors[codename] = str(np.random.uniform())+','+str(np.random.uniform())+','+str(np.random.uniform())
        units[codename] = ' '+str(var.unit.symbol) if var.unit and var.unit.symbol != '' else ''
        vars[codename] = var
    

# now make a single scrollable page with one panel for each entity type/process taxon:
fig = make_subplots(rows=len(etpts), cols=1, 
                    subplot_titles=etpts, 
                    specs=[[{}] for etpt in etpts], 
                    vertical_spacing=0.1/max(1,len(etpts)-1))
for r, etpt in enumerate(etpts):
    codenames[etpt].sort()
    # fake a legend separator:
    fig.add_trace(go.Scatter(name=' ', x=[np.nan], y=[np.nan], mode='lines', line={'color':'rgba(255,255,255,0)'}, showlegend=True))
    fig.add_trace(go.Scatter(name=etpt, x=[np.nan], y=[np.nan], mode='lines', line={'color':'rgba(255,255,255,0)'}, showlegend=True))
    # one legend entry per variable:
    for i,cn in enumerate(codenames[etpt]):
        var = vars[cn]
        vals = traj[var]
        unit = units[cn]
        color = colors[cn]
        # set scale so that y axis goes at most from -a...b for a,b between 1 and 10:
        exp = -np.inf
        for i, y in vals.items():
            exp = max(exp, np.ceil(np.log10(np.max(np.abs(y))))-1)
        scale = 10**exp
        # plot one line for each instance:
        nvals = len(vals.keys())
        if nvals == 0: continue
        # combine all instances' data into one long sequence, separated by nans, 
        # so that they can form a single trace we can toggle with a single click:
        xs = np.zeros((nvals, nts+1)) + np.nan
        ys = np.zeros((nvals, nts+1)) + np.nan
        for i, inst in enumerate(vals.keys()):
            xs[i, :nts] = y = t
            ys[i, :nts] = y = vals[inst]
        if nvals > 1:
            fig.add_trace(go.Scatter(name=cn+(' [%g'%scale)+('*'+unit if unit!='' else '')+']',
                                     x=xs.flatten(), y=ys.flatten()/scale,
                                     mode='lines',  
                                     line={'color':'rgba('+color+',0.5)','width':1},
                                     showlegend=True,
                                     visible='legendonly'
                                     ),
                          row=1+r,col=1)
        # plot a line for the average:
        fig.add_trace(go.Scatter(name=('avg. ' if nvals > 1 else '')+cn+(' [%g'%scale)+unit+']',  # TODO: nicer scale formatting
                                 x=t, y=ys[:, :nts].mean(axis=0)/scale,
                                 mode='lines',  
                                 line={'color':'rgb('+color+')','width':3},
                                 showlegend=True,
                                 visible='legendonly'
                                 ),
                      row=1+r,col=1)
        fig.update_xaxes(row=1+r, col=1, showgrid=False)
        fig.update_yaxes(row=1+r, col=1, showgrid=False)
fig.update_xaxes(title_text='t [yr]', row=1+r, col=1)
fig.update_layout(
    height=720*len(etpts), 
    width=1280,
    plot_bgcolor='rgb(0,0,0)',
    hoverlabel=dict(
        font_size=12,
        namelength=100
    ),
    legend=dict(font=dict(size=16))
)
fig.show()

