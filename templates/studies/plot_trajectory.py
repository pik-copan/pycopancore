# example script for plotting with plotly:
    
# ADJUST FILENAME HERE:
filename = "/tmp/without_social.pickle";
# note: that file should have been produced like in the end of run_example1.py!


from pickle import load
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# load data:
traj = load(open(filename,"rb"))

# extract time points, entity types/process taxa, variable codenames, instances:
t = np.array(traj['t'])
etpts = []
codenames = {}
units = {}
colors = {}
instances = {}
for key, value in traj.items():
    if '.' not in key: continue
    pos = key.index('.')
    etpt = key[:pos]
    codename = key[pos+1:]
    if etpt not in etpts:
        ins = list(value.keys())
        if len(ins)>0:
            etpts.append(etpt)
            codenames[etpt] = []
            instances[etpt] = ins
    if etpt in etpts:
        codenames[etpt].append(codename)
        colors[codename] = str(np.random.uniform())+','+str(np.random.uniform())+','+str(np.random.uniform())
        units[codename] = '' # TODO!

# now make a single scrollable page with one panel for each entity type/process taxon:
fig = make_subplots(rows=len(etpts), cols=1, 
                    subplot_titles=etpts, 
                    specs=[[{}] for etpt in etpts], 
                    vertical_spacing=0.1/(len(etpts)-1))
for r, etpt in enumerate(etpts):
    # fake a legend separator:
    fig.add_trace(go.Scatter(name=' ', x=[np.nan], y=[np.nan], mode='lines', line={'color':'rgba(255,255,255,0)'}, showlegend=True))
    fig.add_trace(go.Scatter(name=etpt, x=[np.nan], y=[np.nan], mode='lines', line={'color':'rgba(255,255,255,0)'}, showlegend=True))
    # one legend entry per variable:
    for cn in codenames[etpt]:
        key = etpt+'.'+cn
        vals = traj[key]
        unit = units[cn]
        color = colors[cn]
        # set scale so that y axis goes at most from -a...b for a,b between 1 and 10:
        exp = -np.inf
        for i, y in vals.items():
            exp = max(exp, np.ceil(np.log10(np.max(np.abs(y))))-1)
        scale = 10**exp
        # plot one line for each instance:
        total = 0
        nvals = len(vals.keys())
        if nvals == 0: continue
        for i, y in vals.items():
            y = np.array(y)
            total += y
            if nvals > 1:
                fig.add_trace(go.Scatter(name=cn+' ('+i+')',
                                         x=t, y=y/scale,
                                         mode='lines',  
                                         line={'color':'rgba('+color+',0.5)','width':1},
                                         showlegend=False,
                                         ),
                              row=1+r,col=1)
        # plot a line for the average:
        fig.add_trace(go.Scatter(name=cn+(' [%g'%scale)+unit+']',  # TODO: nicer scale formatting
                                 x=t, y=total/nvals/scale,
                                 mode='lines',  
                                 line={'color':'rgb('+color+')','width':3},
                                 showlegend=True,
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
