"""Script to plot example2 model results."""

import numpy as np
from numpy import array, average, mean
from pylab import plot, gca, show, figure, subplots, gca, semilogy, legend, \
    tight_layout, NullLocator
from pickle import load

f, ((ax11, ax12), (ax21, ax22), (ax31, ax32)) = \
    subplots(nrows=3, ncols=2, sharex=True, sharey=False, figsize=(12, 12))
lws = 1
al = 0.5

# LEFT: without policy

ax11.title.set_text('example run without socio-cultural processes')

traj = load(open("/home/jobst/work/without.pickle","rb"))
worlds = list(traj["World.atmospheric_carbon"].keys())
social_systems = list(traj["SocialSystem.has_emissions_tax"].keys())
cells = list(traj["Cell.fossil_carbon"].keys())
individuals = list(traj["Individual.is_environmentally_friendly"].keys())
t = np.array(traj['t'])

print(social_systems, cells)

# cultural
ax11.plot(t[3:], 100*average([array(traj["Individual.is_environmentally_friendly"][i][3:]*1) for i in individuals], axis=0,
                             weights=[array(traj["Individual.represented_population"][i][3:]*1) for i in individuals]),
          color="green",lw=2, label="env. friendly individuals")
ax11.plot(t[3:], 1 + 100*mean([array(traj["SocialSystem.has_emissions_tax"][s][3:]*1) for s in social_systems], axis=0),
          color="cyan",lw=2, label="regions w/ emissions tax")
ax11.set_ylabel('CUL:\nglobal opinions & policies\n(percent)')
ax11.set_ylim(-5,105)
# ax11.legend(title='CUL: opinions & policies')
ax11.legend(loc=7)

# metabolic
for i, s in enumerate(social_systems):
    Es = array(traj["SocialSystem.secondary_energy_flow"][s][3:])
    ax21.plot(t[3:], 100*array(traj["SocialSystem.biomass_input_flow"][s][3:]) * 40e9 / Es, 
              color="green", lw=lws, alpha=al, label=None if i else "biomass")
    ax21.plot(t[3:], 100*array(traj["SocialSystem.fossil_fuel_input_flow"][s][3:]) * 47e9 / Es, 
              color="gray", lw=lws, alpha=al, label=None if i else "fossils")
    ax21.plot(t[3:], 100*array(traj["SocialSystem.renewable_energy_input_flow"][s][3:]) / Es, 
              color="darkorange", lw=lws, alpha=al, label=None if i else "renewables")
ax21.set_ylabel('MET:\nregional energy shares\n(percent)')
ax21.set_ylim(-5,105)
#ax21.legend(title='MET: regional energy shares')
ax21.legend(loc=7)

# environmental
ax31.plot(t[3:], traj["World.atmospheric_carbon"][worlds[0]][3:], 
          color="cyan", lw=2, label="atmosphere")
ax31.plot(t[3:], traj["World.upper_ocean_carbon"][worlds[0]][3:], 
          color="blue", lw=2, label="upper oceans")
ax31.plot(t[3:], sum(array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells), 
          color="green", lw=2, label="plants & soils")
ax31.plot(t[3:], sum(array(traj["Cell.fossil_carbon"][c][3:]) for c in cells), 
          color="gray", lw=2, label="fossils")
ax31.set_ylabel('ENV:\nglobal carbon stocks\n(gigatonnes carbon)')
ax31.set_ylim(-100,3100)
#ax31.legend(title='ENV: global carbon stocks')
ax31.legend(loc=7)

ax31.set_xlabel('year')
ax31.set_xlim(1990,2110)

# RIGHT: with policy

ax12.title.set_text('example run with socio-cultural processes')

traj = load(open("/home/jobst/work/with.pickle","rb"))
worlds = list(traj["World.atmospheric_carbon"].keys())
social_systems = list(traj["SocialSystem.has_emissions_tax"].keys())
cells = list(traj["Cell.fossil_carbon"].keys())
individuals = list(traj["Individual.is_environmentally_friendly"].keys())
t = np.array(traj['t'])

print((s,traj["SocialSystem.has_emissions_tax"][s]) for s in social_systems)

# cultural
ax12.plot(t[3:], 100*average([array(traj["Individual.is_environmentally_friendly"][i][3:]*1) for i in individuals], axis=0,
                             weights=[array(traj["Individual.represented_population"][i][3:]*1) for i in individuals]),
          color="green",lw=2, label="env. friendly individuals")
ax12.plot(t[3:], 100*mean([array(traj["SocialSystem.has_emissions_tax"][s][3:]*1) for s in social_systems], axis=0),
          color="cyan",lw=2, label="regions w/ emissions tax")
ax12.set_ylim(-5,105)
ax12.yaxis.set_major_locator(NullLocator())
ax12.legend(loc=7)

# metabolic
for i, s in enumerate(social_systems):
    Es = array(traj["SocialSystem.secondary_energy_flow"][s][3:])
    ax22.plot(t[3:], 100*array(traj["SocialSystem.biomass_input_flow"][s][3:]) * 40e9 / Es, 
              color="green", lw=lws, alpha=al, label=None if i else "biomass")
    ax22.plot(t[3:], 100*array(traj["SocialSystem.fossil_fuel_input_flow"][s][3:]) * 47e9 / Es, 
              color="gray", lw=lws, alpha=al, label=None if i else "fossils")
    ax22.plot(t[3:], 100*array(traj["SocialSystem.renewable_energy_input_flow"][s][3:]) / Es, 
              color="darkorange", lw=lws, alpha=al, label=None if i else "renewables")
ax22.set_ylim(-5,105)
ax22.yaxis.set_major_locator(NullLocator())
ax22.legend(loc=7)

# environmental
ax32.plot(t[3:], traj["World.atmospheric_carbon"][worlds[0]][3:], 
          color="cyan", lw=2, label="atmosphere")
ax32.plot(t[3:], traj["World.upper_ocean_carbon"][worlds[0]][3:], 
          color="blue", lw=2, label="upper oceans")
ax32.plot(t[3:], sum(array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells), 
          color="green", lw=2, label="plants & soils")
ax32.plot(t[3:], sum(array(traj["Cell.fossil_carbon"][c][3:]) for c in cells), 
          color="gray", lw=2, label="fossils")
ax32.yaxis.set_major_locator(NullLocator())
ax32.set_ylim(-100,3100)

ax32.set_xlabel('year')
ax32.set_xlim(1990,2110)
ax32.legend(loc=7)

f.subplots_adjust(hspace=0, wspace=0)
show()

