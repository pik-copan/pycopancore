"""Skript to plot Jobsts prototype model results."""

import numpy as np
from numpy import array, average, mean
from pylab import plot, gca, show, figure, subplot, gca, semilogy, legend
from pickle import load

traj = load(open("/home/jobst/work/with.pickle","rb"))
worlds = list(traj["atmospheric_carbon"].keys())
societies = list(traj["population"].keys())
cells = list(traj["fossil_carbon"].keys())
individuals = list(traj["is_environmentally_friendly"].keys())
t = np.array(traj['t'])

figure()
lws = 1
al = 0.5

subplot(411)  # cultural
plot(t[3:], 100*average([array(traj["is_environmentally_friendly"][i][3:]*1) for i in individuals], axis=0,
                        weights=[array(traj["represented_population"][i][3:]*1) for i in individuals]
                        ),color="green",lw=lws, label="environmentally friendly individuals")
plot(t[3:], 100*mean([array(traj["has_renewable_subsidy"][s][3:]*1) for s in societies], axis=0),color="darkorange",lw=lws, label="societies with renewable subsidy")
plot(t[3:], 100*mean([array(traj["has_emissions_tax"][s][3:]*1) for s in societies], axis=0),color="blue",lw=lws, label="societies with emissions tax")
plot(t[3:], 100*mean([array(traj["has_fossil_ban"][s][3:]*1) for s in societies], axis=0),color="gray",lw=lws, label="societies with fossil ban")
gca().set_ylabel('percent')
legend()

subplot(412)  # metabolic, logscale: capital, knowledge, production, wellbeing
ax1 = gca()
ax1.set_ylabel('per-cap. dollars per year', color="magenta")
ax1.tick_params('y', colors="magenta")
ax2 = ax1.twinx()
ax2.set_ylabel('petajoules', color='darkorange')
ax2.tick_params('y', colors='darkorange')
for i, s in enumerate(societies):
    ax1.plot(t[3:], array(traj["wellbeing"][s][3:]), color="magenta", lw=lws, alpha=al, label=None if i else "regional wellbeing")
    ax2.semilogy(t[3:], array(traj["renewable_energy_knowledge"][s][3:])/1e6, color="darkorange", lw=lws, alpha=al, 
                 label=None if i else "regional renewable energy knowledge")
ax1.plot(t[3:], average([array(traj["wellbeing"][s][3:]) for s in societies], axis=0,
                        weights=[array(traj["population"][s][3:]) for s in societies]), 
         color="magenta", lw=3, label="avg. wellbeing")
ax2.semilogy(t[3:], sum(array(traj["renewable_energy_knowledge"][s][3:])/1e6 for s in societies), color="darkorange", lw=3,
             label="total renewable energy knowledge")
ax1.legend(loc=2)
ax2.legend(loc=1)

subplot(413)  # metabolic: energy mix
for i, s in enumerate(societies):
    Es = array(traj["secondary_energy_flow"][s][3:])
    plot(t[3:], 100*array(traj["biomass_input_flow"][s][3:]) * 40e9 / Es, color="green", lw=lws, alpha=al, label=None if i else "regional share of biomass energy")
    plot(t[3:], 100*array(traj["fossil_fuel_input_flow"][s][3:]) * 47e9 / Es, color="gray", lw=lws, alpha=al, label=None if i else "regional share of fossil energy")
    plot(t[3:], 100*array(traj["renewable_energy_input_flow"][s][3:]) / Es, color="darkorange", lw=lws, alpha=al, label=None if i else "regional share of renewables")
plot(t[3:], 100*average([array(traj["biomass_input_flow"][s][3:]) for s in societies], axis=0,
                        weights=[array(traj["population"][s][3:]) for s in societies]) * 40e9 / Es, color="green", lw=3, label="global share of biomass energy")
plot(t[3:], 100*average([array(traj["fossil_fuel_input_flow"][s][3:]) for s in societies], axis=0,
                        weights=[array(traj["population"][s][3:]) for s in societies]) * 47e9 / Es, color="gray", lw=3, label="global share of fossil energy")
plot(t[3:], 100*average([array(traj["renewable_energy_input_flow"][s][3:]) for s in societies], axis=0,
                        weights=[array(traj["population"][s][3:]) for s in societies]) / Es, color="darkorange", lw=3, label="global share of renewables")
gca().set_ylabel('percent')
legend()

subplot(414)  # natural
plot(t[3:], traj["atmospheric_carbon"][worlds[0]][3:], color="cyan", lw=3, label="atmospheric carbon")
plot(t[3:], traj["upper_ocean_carbon"][worlds[0]][3:], color="blue", lw=3, label="upper ocean carbon")
plot(t[3:], sum(array(traj["terrestrial_carbon"][c][3:]) for c in cells), color="green", lw=3, label="terrestrial carbon")
plot(t[3:], sum(array(traj["fossil_carbon"][c][3:]) for c in cells), color="gray", lw=3, label="fossil carbon")
#for i, s in enumerate(societies):
#    plot(t[3:], traj["protected_terrestrial_carbon"][s][3:],color="green",lw=lws, label=None if i else "protected biomass")
gca().set_ylabel('gigatonnes carbon')
legend()

show()

# TODO: 
# policy shares, env. friendly shares
# transparancy, means
# wellb. abs., renew., pop. log
# total protected
# horiz.
# save dump with codename,uid as key