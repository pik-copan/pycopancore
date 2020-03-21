#!/usr/bin/env python
# coding: utf-8
import numpy as np
from matplotlib import pyplot as plt

AX1_PLOTS = (("terr", "g", "Terrestrial carbon"),
             ("atmo", "c", "Atmospheric carbon"),
             ("ocea", "b", "Ocean carbon"))

def main():

    _, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 8))
    ax3 = ax2.twinx()

    results = np.load("results_ensemble.p", allow_pickle=True)
    baseline = np.load("esd_example_without_social_seed_0.p", allow_pickle=True)

    keys = [k for k in results.keys() if isinstance(k, float)]
    keys.sort()

    for shortlabel, color, label in AX1_PLOTS:
        _y = np.zeros((len(keys), 2))
        for i, key in enumerate(keys):
            _y[i, 0] = np.mean(results[key][shortlabel])
            _y[i, 1] = np.std(results[key][shortlabel])
        ax1.errorbar(keys, _y[:, 0], yerr=_y[:, 1], fmt='o', c=color,
                     alpha=0.5, label=label)


    gmt = np.zeros((len(keys), 2))
    econ = np.zeros((len(keys), 4))
    for i, key in enumerate(keys):
        gmt[i, 0] = np.mean(results[key]["gmt"])
        gmt[i, 1] = np.std(results[key]["gmt"])
        econ[i, 0:2] = np.mean(results[key]["econ"], axis=0)
        econ[i, 2:] = np.std(results[key]["econ"], axis=0)

    econ[:, 0::2] /= 0.25 * 6e9
    econ[:, 1::2] /= 0.75 * 6e9

    ax2.errorbar(keys, econ[:, 0], yerr=econ[:, 2], fmt='o', c="r",
                 alpha=0.5, label="North")
    ax2.errorbar(keys, econ[:, 1], yerr=econ[:, 3], fmt='d', c="r",
                 alpha=0.5, label="South")

    ax3.errorbar(keys, gmt[:, 0], yerr=gmt[:, 1], fmt='o', c="k",
                 alpha=0.5, label="Global Mean Temperature")

    world = list(baseline["World.surface_air_temperature"].keys())[0]

    _y = baseline["World.terrestrial_carbon"][world][-1]
    ax1.axhline(_y, c="g", ls="--", lw=2)

    _y = baseline["World.atmospheric_carbon"][world][-1]
    ax1.axhline(_y, c="c", ls="--", lw=2)

    _y = baseline["World.upper_ocean_carbon"][world][-1]
    ax1.axhline(_y, c="b", ls="--", lw=2)

    social_systems = list(baseline["SocialSystem.has_emissions_tax"].keys())
    _y = [baseline["SocialSystem.economic_output_flow"][s][-1] for s in social_systems]
    ax2.axhline(_y[0] / 0.25 / 6e9, ls="--", lw=2, c="r")
    ax2.axhline(_y[1] / 0.75 / 6e9, ls="--", lw=2, c="r")

    _y = baseline["World.surface_air_temperature"][world][-1]
    ax3.axhline(_y, c="k", ls="--", lw=2)

    ax1.legend()
    ax2.legend(loc="center left")
    ax3.legend(loc="upper left")

    ax2.set_xlabel("Learning rate [$yr^{-1}$]")

    ax1.set_ylabel("Gigatonnes Carbon in 2120")
    ax2.set_ylabel("GDP/capita in 2120 [$/yr]")
    ax3.set_ylabel("Global mean temperature in 2120 [K]")

    ax2.semilogx()
    ax2.semilogy()
    ax2.set_xlim(min(keys), max(keys))

    ax3.set_ylim(287.5, 290)

    plt.tight_layout()
    plt.savefig("figure6.pdf")


if __name__ == "__main__":
    main()
