"""Script to plot example2 model results."""
from pickle import load
import matplotlib
matplotlib.use("Agg")
import numpy as np
from numpy import array, mean
from matplotlib import pyplot as plt

lws = 2
al = 1.
ls = ["-", ":"]

def plot_one_row(infile, axarr):

    ax1, ax2, ax3, ax4 = axarr

    traj = load(open(infile,"rb"))
    worlds = list(traj["World.atmospheric_carbon"].keys())
    social_systems = list(traj["SocialSystem.has_fossil_ban"].keys())
    cells = list(traj["Cell.fossil_carbon"].keys())
    individuals = list(traj["Individual.is_environmentally_friendly"].keys())
    t = np.array(traj['t'])
   
    share_env_friendly = [np.array(traj["Individual.is_environmentally_friendly"][i][3:]*1) for i in individuals]
    weights = [np.array(traj["Individual.represented_population"][i][3:]*1) for i in individuals]
    share_env_friendly = 100 * np.average(share_env_friendly, weights=weights, axis=0)
    ax1.plot(t[3:], share_env_friendly, color="green",lw=2, 
              label="env. friendly individuals")

    has_fossil_ban = 1 + 100*mean([array(traj["SocialSystem.has_fossil_ban"][s][3:]*1) for s in social_systems], axis=0)
    ax1.plot(t[3:], has_fossil_ban, color="cyan",lw=2, 
              label="regions w/subsidy and fossil ban")

    for i, s in enumerate(social_systems):
        energy_flow = array(traj["SocialSystem.secondary_energy_flow"][s][3:])
        biomass_flow = 100 * array(traj["SocialSystem.biomass_input_flow"][s][3:]) * 40e9 / energy_flow
        fossil_flow = 100 * array(traj["SocialSystem.fossil_fuel_input_flow"][s][3:]) * 47e9 / energy_flow
        renewable_flow = 100 * array(traj["SocialSystem.renewable_energy_input_flow"][s][3:]) / energy_flow
        ax2.plot(t[3:], biomass_flow, color="green", ls=ls[i], lw=lws, alpha=al, label=None if i else "biomass")
        ax2.plot(t[3:], fossil_flow, color="gray", ls=ls[i], lw=lws, alpha=al, label=None if i else "fossils")
        ax2.plot(t[3:], renewable_flow, color="darkorange", ls=ls[i], lw=lws, alpha=al, label=None if i else "renewables")
    
   
    # Left column, third row: GPD without social processes
    for i, s in enumerate(social_systems):
        economic_flow = 100*array(traj["SocialSystem.economic_output_flow"][s][3:]) / [0.25, 0.75][i] / 6e9
        ax3.plot(t[3:], economic_flow, color="red", ls=ls[i], lw=lws, alpha=al, label=None if i else "GDP")

    ax3.semilogy()
   
    # Left column, forth row: Environment without social processes
    atmos_carb = traj["World.atmospheric_carbon"][worlds[0]][3:]
    ocean_carb = traj["World.upper_ocean_carbon"][worlds[0]][3:]
    terre_carb = sum(array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells)
    fossi_carb = sum(array(traj["Cell.fossil_carbon"][c][3:]) for c in cells)
    #photosynth = 10 * sum(array(traj["Cell.photosynthesis_carbon_flow"][c][3:]) for c in cells)
    
    print((atmos_carb+terre_carb+ocean_carb)[-1])
    ax4.plot(t[3:], atmos_carb,
             color="cyan", lw=2, label="atmosphere")
    ax4.plot(t[3:], ocean_carb,
             color="blue", lw=2, label="upper oceans")
    ax4.plot(t[3:], terre_carb,
             color="green", lw=2, label="plants & soils")
    ax4.plot(t[3:], fossi_carb,
             color="gray", lw=2, label="fossils")
    
   
    ax1.set_ylim(-5,105)
    ax2.set_ylim(-5,105)
   
    ax4.set_ylim(-100,3500)
    ax4.set_xlabel('model year')
    ax4.set_xlim(2000, 2120)
    ax4.set_xticks(ticks=np.arange(2000, 2130, 20))
    ax4.set_xticklabels(np.arange(0, 130, 20))

def main():

    with_file = "esd_example_with_social_update_rate_12.0_seed_0.p"
    wo_file = "esd_example_without_social_seed_0.p"
    
    f, axarr = plt.subplots(nrows=4, ncols=2, sharex=True, figsize=(12, 14))
   
    plot_one_row(wo_file, axarr[:, 0]) 
    plot_one_row(with_file, axarr[:, 1])

    axarr[0, 0].title.set_text('example run without socio-cultural processes')
    axarr[0, 1].title.set_text('example run with socio-cultural processes')

    axarr[0, 0].set_ylabel('CUL:\nglobal opinions & policies\n(percent)')
    axarr[0, 0].legend(loc=7)

    axarr[1, 0].set_ylabel('MET:\nregional energy shares\n(percent)')
    axarr[1, 0].legend()

    axarr[2, 0].set_ylabel('MET:\nGDP/capita ($/yr)')

    axarr[3, 0].set_ylabel('ENV:\nglobal carbon stocks\n(gigatonnes carbon)')
    axarr[3, 0].legend(loc="upper left")

    for ax in axarr[:, 1]:
        plt.setp(ax.get_yticklabels(), visible=False)

    plt.tight_layout()
    plt.savefig("figure5.pdf")


if __name__ == "__main__":
    main()
