"""Script to plot example2 model results."""

import numpy as np
from numpy import array, average, mean
from pylab import plot, gca, show, figure, subplots, gca, semilogy, legend, \
    tight_layout, NullLocator, savefig
from pickle import load

with_file = "/home/leander/Dokumente/Studium/13/Masterthesis/pycopancore/simulation_results/with.pickle"
wo_file = "/home/leander/Dokumente/Studium/13/Masterthesis/pycopancore/simulation_results/without.pickle"


f, ((ax11, ax12), (ax21, ax22), (ax2b1, ax2b2), (ax31, ax32)) = \
    subplots(nrows=4, ncols=2, sharex=True, sharey=False, figsize=(12, 12))
lws = 1
al = 0.5
lss = ['-','--']


# LEFT: without policy

ax11.title.set_text('example run without socio-cultural processes')

traj = load(open(wo_file,"rb"))
worlds = list(traj["World.atmospheric_carbon"].keys())
social_systems = list(traj["SocialSystem.has_emissions_tax"].keys())
cells = list(traj["Cell.fossil_carbon"].keys())
individuals = list(traj["Individual.is_environmentally_friendly"].keys())
t = np.array(traj['t'])

print(social_systems, cells)

# cultural
for i, s in enumerate(social_systems):
    ax11.plot(t[3:], 100*average([array(traj["Individual.is_environmentally_friendly"][ii][3:]*1) for j, ii in enumerate(individuals) if (j%4)//2 == i], axis=0,
                                 weights=[array(traj["Individual.represented_population"][ii][3:]*1) for j, ii in enumerate(individuals) if (j%4)//2 == i]),
              color="green",lw=1, linestyle=lss[i], label=None if i else "env. friendly individuals")
ax11.plot(t[3:], 1 + 100*mean([array(traj["SocialSystem.has_emissions_tax"][s][3:]*1) for s in social_systems], axis=0),
          color="cyan",lw=2, label="regions w/ emissions tax")
ax11.set_ylabel('CUL:\nregional opinions & policies\n(percent)')
ax11.set_ylim(-5,105)
# ax11.legend(title='CUL: opinions & policies')
#ax11.legend(loc=7)

# metabolic
for i, s in enumerate(social_systems):
    Es = array(traj["SocialSystem.secondary_energy_flow"][s][3:])
    ax21.plot(t[3:], 100*array(traj["SocialSystem.biomass_input_flow"][s][3:]) * 40e9 / Es, 
              color="green", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "biomass")
    ax21.plot(t[3:], 100*array(traj["SocialSystem.fossil_fuel_input_flow"][s][3:]) * 47e9 / Es, 
              color="gray", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "fossils")
    ax21.plot(t[3:], 100*array(traj["SocialSystem.renewable_energy_input_flow"][s][3:]) / Es, 
              color="darkorange", lw=lws, linestyle=lss[i], alpha=al, label=None if i else "renewables")
    ax2b1.semilogy(t[3:], array(traj["SocialSystem.economic_output_flow"][s][3:]) 
                                / array(traj["SocialSystem.population"][s][3:]), 
              color="magenta", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "GDP per capita [USD/yr]")
    ax2b1.semilogy(t[3:], 1e-9 * array(traj["SocialSystem.physical_capital"][s][3:]), 
              color="black", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "physical capital [bln. USD]")
ax21.set_ylabel('MET:\nregional energy shares\n(percent)')
ax21.set_ylim(-5,105)
ax2b1.set_ylim(.9e4,1.1e6)
#ax21.legend(title='MET: regional energy shares')
#ax21.legend(loc=7)

ax2b1.set_ylabel('MET:\neconomic production\n(log-scale)')
#ax2b1.set_ylim(-5,105)
#ax21.legend(title='MET: regional energy shares')
#ax2b1.legend(loc=7)

# environmental
ax31.plot(t[3:], traj["World.atmospheric_carbon"][worlds[0]][3:], 
          color="cyan", lw=2, label="atmosphere (global)")
ax31.plot(t[3:], traj["World.upper_ocean_carbon"][worlds[0]][3:], 
          color="blue", lw=2, label="upper oceans (global)")
#ax31.plot(t[3:], sum(array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells), 
#          color="green", lw=2, label="plants & soils")
#ax31.plot(t[3:], sum(array(traj["Cell.fossil_carbon"][c][3:]) for c in cells), 
#          color="gray", lw=2, label="fossils")
for i, c in enumerate(cells):
    ax31.plot(t[3:], array(traj["Cell.terrestrial_carbon"][c][3:]), 
              color="green", lw=1, linestyle=lss[i//2], label=None if i else "plants & soils (per cell)")
    ax31.plot(t[3:], array(traj["Cell.fossil_carbon"][c][3:]), 
              color="gray", lw=1, linestyle=lss[i//2], label=None if i else "fossils (per cell)")
ax31.set_ylabel('ENV:\ncarbon stocks\n(gigatonnes carbon)')
ax31.set_ylim(-100,1300) #3100)
#ax31.legend(title='ENV: global carbon stocks')
#ax31.legend(loc=7)

ax31.set_xlabel('year')
ax31.set_xlim(1990,2110)


# RIGHT: with policy

ax12.title.set_text('example run with socio-cultural processes')

traj = load(open(with_file,"rb"))
worlds = list(traj["World.atmospheric_carbon"].keys())
social_systems = list(traj["SocialSystem.has_emissions_tax"].keys())
cells = list(traj["Cell.fossil_carbon"].keys())
individuals = list(traj["Individual.is_environmentally_friendly"].keys())
t = np.array(traj['t'])

print((s,traj["SocialSystem.has_emissions_tax"][s]) for s in social_systems)

# cultural
for i, s in enumerate(social_systems):
    ax12.plot(t[3:], 100*average([array(traj["Individual.is_environmentally_friendly"][ii][3:]*1) for j, ii in enumerate(individuals) if (j%4)//2 == i], axis=0,
                                 weights=[array(traj["Individual.represented_population"][ii][3:]*1) for j, ii in enumerate(individuals) if (j%4)//2 == i]),
              color="green",lw=1, linestyle=lss[i], label=None if i else "env. friendly individuals")
ax12.plot(t[3:], 100*mean([array(traj["SocialSystem.has_emissions_tax"][s][3:]*1) for s in social_systems], axis=0),
          color="cyan",lw=2, label="regions w/ emissions tax")
ax12.set_ylim(-5,105)
ax12.yaxis.set_major_locator(NullLocator())
ax12.legend(loc=7)

# metabolic
for i, s in enumerate(social_systems):
    Es = array(traj["SocialSystem.secondary_energy_flow"][s][3:])
    ax22.plot(t[3:], 100*array(traj["SocialSystem.biomass_input_flow"][s][3:]) * 40e9 / Es, 
              color="green", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "biomass")
    ax22.plot(t[3:], 100*array(traj["SocialSystem.fossil_fuel_input_flow"][s][3:]) * 47e9 / Es, 
              color="gray", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "fossils")
    ax22.plot(t[3:], 100*array(traj["SocialSystem.renewable_energy_input_flow"][s][3:]) / Es, 
              color="darkorange", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "renewables")
    ax2b2.semilogy(t[3:], array(traj["SocialSystem.economic_output_flow"][s][3:]) 
                                / array(traj["SocialSystem.population"][s][3:]), 
              color="magenta", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "GDP per capita [USD/yr]")
    ax2b2.semilogy(t[3:], 1e-9 * array(traj["SocialSystem.physical_capital"][s][3:]), 
              color="black", lw=lws, alpha=al, linestyle=lss[i], label=None if i else "physical capital [bln. USD]")
ax22.set_ylim(-5,105)
ax2b2.set_ylim(.9e4,1.1e6)
ax22.yaxis.set_major_locator(NullLocator())
ax2b2.yaxis.set_major_locator(NullLocator())
ax22.legend(loc=7)
ax2b2.legend(loc=8)

# environmental
ax32.plot(t[3:], traj["World.atmospheric_carbon"][worlds[0]][3:], 
          color="cyan", lw=2, label="atmosphere")
ax32.plot(t[3:], traj["World.upper_ocean_carbon"][worlds[0]][3:], 
          color="blue", lw=2, label="upper oceans")
#ax32.plot(t[3:], sum(array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells), 
#          color="green", lw=2, label="plants & soils")
#ax32.plot(t[3:], sum(array(traj["Cell.fossil_carbon"][c][3:]) for c in cells), 
#          color="gray", lw=2, label="fossils")
for i, c in enumerate(cells):
    ax32.plot(t[3:], array(traj["Cell.terrestrial_carbon"][c][3:]), 
              color="green", lw=1, linestyle=lss[i//2], label=None if i else "plants & soils (per cell)")
    ax32.plot(t[3:], array(traj["Cell.fossil_carbon"][c][3:]), 
              color="gray", lw=1, linestyle=lss[i//2], label=None if i else "fossils (per cell)")

ax32.yaxis.set_major_locator(NullLocator())
ax32.set_ylim(-100,1300) #3100)

ax32.set_xlabel('year')
ax32.set_xlim(1990,2110)
ax32.legend(loc=8)

f.subplots_adjust(hspace=0, wspace=0)
savefig(with_file+".pdf")

