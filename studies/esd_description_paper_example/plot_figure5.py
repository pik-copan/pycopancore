"""Script to plot example2 model results."""

from pickle import load
import numpy as np
from matplotlib import pyplot as plt

LINEWIDTH = 2
LINESTYLES = ["-", ":"]


def plot_one_row(infile, axarr):

    traj = load(open(infile, "rb"))

    worlds = list(traj["World.atmospheric_carbon"].keys())
    social_systems = list(traj["SocialSystem.has_fossil_ban"].keys())
    cells = list(traj["Cell.fossil_carbon"].keys())
    individuals = list(traj["Individual.is_environmentally_friendly"].keys())

    time = np.array(traj["t"])

    _y = [
        traj["Individual.is_environmentally_friendly"][i][3:]
        for i in individuals
    ]  # noqa: E501
    _w = [
        traj["Individual.represented_population"][i][3:] for i in individuals
    ]  # noqa: E501
    _y = 100 * np.average(_y, weights=_w, axis=0)
    axarr[0].plot(
        time[3:], _y, color="green", lw=2, label="env. friendly individuals"
    )  # noqa: E501

    _y = [traj["SocialSystem.has_fossil_ban"][s][3:] for s in social_systems]
    _y = 1 + 100 * np.mean(_y, axis=0)
    axarr[0].plot(
        time[3:],
        _y,
        color="cyan",
        lw=2,
        label="regions w/subsidy and fossil ban",  # noqa: E501
    )

    for i, soc in enumerate(social_systems):
        energy_flow = np.array(
            traj["SocialSystem.secondary_energy_flow"][soc][3:]
        )  # noqa: E501

        _y = np.array(traj["SocialSystem.biomass_input_flow"][soc][3:])
        _y = 100 * _y * 40e9 / energy_flow
        axarr[1].plot(
            time[3:],
            _y,
            color="green",
            ls=LINESTYLES[i],
            lw=LINEWIDTH,
            label=None if i else "biomass",
        )

        _y = np.array(traj["SocialSystem.fossil_fuel_input_flow"][soc][3:])
        _y = 100 * _y * 47e9 / energy_flow
        axarr[1].plot(
            time[3:],
            _y,
            color="gray",
            ls=LINESTYLES[i],
            lw=LINEWIDTH,
            label=None if i else "fossils",
        )

        _y = np.array(
            traj["SocialSystem.renewable_energy_input_flow"][soc][3:]
        )
        _y = 100 * _y / energy_flow
        axarr[1].plot(
            time[3:],
            _y,
            color="darkorange",
            ls=LINESTYLES[i],
            lw=LINEWIDTH,
            label=None if i else "renewables",
        )

    for i, soc in enumerate(social_systems):
        _y = np.array(traj["SocialSystem.economic_output_flow"][soc][3:])
        _y = 100 * _y / [0.25, 0.75][i] / 6e9
        axarr[2].plot(
            time[3:],
            _y,
            color="red",
            ls=LINESTYLES[i],
            lw=LINEWIDTH,
            label=None if i else "GDP",
        )

    _y = traj["World.atmospheric_carbon"][worlds[0]][3:]
    axarr[3].plot(time[3:], _y, color="cyan", lw=2, label="atmosphere")

    _y = traj["World.upper_ocean_carbon"][worlds[0]][3:]
    axarr[3].plot(time[3:], _y, color="blue", lw=2, label="upper oceans")

    _y = sum(np.array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells)
    axarr[3].plot(time[3:], _y, color="green", lw=2, label="plants & soils")

    _y = sum(np.array(traj["Cell.fossil_carbon"][c][3:]) for c in cells)
    axarr[3].plot(time[3:], _y, color="gray", lw=2, label="fossils")

    axarr[0].set_ylim(-5, 105)
    axarr[1].set_ylim(-5, 105)
    axarr[3].set_ylim(-100, 3500)

    axarr[2].semilogy()

    axarr[3].set_xlabel("model year")
    axarr[3].set_xlim(2000, 2120)
    axarr[3].set_xticks(ticks=np.arange(2000, 2130, 20))
    axarr[3].set_xticklabels(np.arange(0, 130, 20))


def main():

    with_file = "esd_example_with_social_update_rate_12.0_seed_0.p"
    wo_file = "esd_example_without_social_seed_0.p"

    _, axarr = plt.subplots(nrows=4, ncols=2, sharex=True, figsize=(12, 14))

    plot_one_row(wo_file, axarr[:, 0])
    plot_one_row(with_file, axarr[:, 1])

    axarr[0, 0].title.set_text("example run without socio-cultural processes")
    axarr[0, 1].title.set_text("example run with socio-cultural processes")

    axarr[0, 0].set_ylabel("CUL:\nglobal opinions & policies\n(percent)")
    axarr[0, 0].legend(loc=7)

    axarr[1, 0].set_ylabel("MET:\nregional energy shares\n(percent)")
    axarr[1, 0].legend()

    axarr[2, 0].set_ylabel("MET:\nGDP/capita ($/yr)")

    axarr[3, 0].set_ylabel("ENV:\nglobal carbon stocks\n(gigatonnes carbon)")
    axarr[3, 0].legend(loc="upper left")

    for axs in axarr[:, 1]:
        plt.setp(axs.get_yticklabels(), visible=False)

    plt.tight_layout()
    plt.savefig("figure5.pdf")


if __name__ == "__main__":
    main()
