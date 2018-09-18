import numpy as np
from numpy import array, average, mean
from pylab import plot, gca, show, figure, subplots, gca, semilogy, legend, \
    tight_layout, NullLocator
from pickle import load


# load data and list keys:

traj = load(open("/tmp/with.pickle","rb")) # TODO: adjust filename
#traj = load(open("/tmp/without.pickle","rb")) # TODO: adjust filename
# traj is a dict of dicts of lists of variable values.
# traj[variable_name] is a dict of lists of variable values for that variable.
# traj[variable_name][entity_label] is a list of variable values for that variable and entity,
# traj[variable_name][entity_label][index] is the value of that variable at that entity 
#    at the time point traj['t'][index]

variables = list(traj.keys())
print("VARIABLES:\n ","\n  ".join(variables))
worlds = list(traj["World.atmospheric_carbon"].keys())
print("Worlds:",worlds)
social_systems = list(traj["SocialSystem.population"].keys())
print("SocialSystems:",social_systems)
cells = list(traj["Cell.fossil_carbon"].keys())
print("Cells:",cells)
individuals = list(traj["Individual.is_environmentally_friendly"].keys())
print("Individuals:",individuals)
t = np.array(traj['t'])
tminmax = [np.min(t),np.max(t)]
print("Timespan:",tminmax)


# specify global and regional boundaries:

# planetary boundary for climate change:
max_World_atmospheric_carbon = 945 # [gigatonnes_carbon]
# planetary boundary for land system change:
min_World_terrestrial_carbon = 2400 # [gigatonnes_carbon]
# planetary boundary for ocean acidification:
max_World_upper_ocean_carbon = 1200 # [gigatonnes_carbon]

# social foundation for wellbeing:
min_wellbeing = 700 # [dollars/year/person], corresponds to the worldbank's 1.90 USD/day powerty line


# prepare a summarizing plot of time evolution:
f, (ax12, ax22, ax22b, ax32) = \
    subplots(nrows=4, ncols=1, sharex=True, sharey=False)
lws = 0.5
al = 0.5

# cultural
ax12.plot(t[3:], 100*average([array(traj["Individual.is_environmentally_friendly"][i][3:]*1) for i in individuals], axis=0,
                        weights=[array(traj["Individual.represented_population"][i][3:]*1) for i in individuals]
                        ),color="green",lw=lws, label="env. friendly individuals")
ax12.plot(t[3:], 100*mean([array(traj["SocialSystem.has_renewable_subsidy"][s][3:]*1) for s in social_systems], axis=0),color="darkorange",lw=2, label="regions w/ renewable subsidy")
ax12.plot(t[3:], 100*mean([array(traj["SocialSystem.has_emissions_tax"][s][3:]*1) for s in social_systems], axis=0),color="blue",lw=2, label="regions w/ emissions tax")
ax12.plot(t[3:], 100*mean([array(traj["SocialSystem.has_fossil_ban"][s][3:]*1) for s in social_systems], axis=0),color="gray",lw=2, label="regions w/ fossil ban")
ax12.set_ylabel('percent')
ax12.set_ylim(-5,105)

# metabolic
for i, s in enumerate(social_systems):
    Es = array(traj["SocialSystem.secondary_energy_flow"][s][3:])
    ax22.plot(t[3:], 100*array(traj["SocialSystem.biomass_input_flow"][s][3:]) * 40e9 / Es, color="green", lw=lws, alpha=al, label=None if i else "biomass")
    ax22.plot(t[3:], 100*array(traj["SocialSystem.fossil_fuel_input_flow"][s][3:]) * 47e9 / Es, color="gray", lw=lws, alpha=al, label=None if i else "fossils")
    ax22.plot(t[3:], 100*array(traj["SocialSystem.renewable_energy_input_flow"][s][3:]) / Es, color="darkorange", lw=lws, alpha=al, label=None if i else "renewables")
    ax22b.plot(t[3:], .001*array(traj["SocialSystem.wellbeing"][s][3:]), color="magenta", lw=2*lws, alpha=al, label=None if i else "wellbeing")
ax22b.plot(tminmax, .001*np.repeat(min_wellbeing,2), "--", color="magenta", lw=2*lws, alpha=al, label="min")
ax22.set_ylabel('percent')
ax22b.set_ylabel('1000 USD/year/person')
ax22.set_ylim(-5,105)

# environmental
ax32.plot(t[3:], traj["World.atmospheric_carbon"][worlds[0]][3:], color="cyan", lw=2, label="atmosphere")
ax32.plot(tminmax, np.repeat(max_World_atmospheric_carbon,2), "--", color="cyan", lw=1, label="max")
ax32.plot(t[3:], traj["World.upper_ocean_carbon"][worlds[0]][3:], color="blue", lw=2, label="upper oceans")
ax32.plot(tminmax, np.repeat(max_World_upper_ocean_carbon,2), "--", color="blue", lw=1, label="max")
ax32.plot(t[3:], sum(array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells), color="green", lw=2, label="plants & soils")
ax32.plot(tminmax, np.repeat(min_World_terrestrial_carbon,2), "--", color="green", lw=1, label="min")
ax32.plot(t[3:], sum(array(traj["Cell.fossil_carbon"][c][3:]) for c in cells), color="gray", lw=2, label="fossils")
ax32.set_ylabel('gigatonnes carbon')
ax32.set_ylim(-100,3100)

ax32.set_xlabel('year')
#ax32.set_xlim(1990,2110)

ax12.legend(title='CUL: opinions & policies')
ax22.legend(title='MET: energy shares')
ax22b.legend(title='MET: wellbeing')
ax32.legend(title='ENV: global carbon stocks')

f.subplots_adjust(hspace=0, wspace=0)
show()

