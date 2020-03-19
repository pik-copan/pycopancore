#!/usr/bin/env python
# coding: utf-8
import matplotlib
matplotlib.use("Agg")

import numpy as np
from os import listdir
import glob
from matplotlib import pyplot as plt
import pickle

f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6,8))

results = np.load("results_ensemble.p")

keys = [k for k in results.keys() if isinstance(k, float)]
keys.sort()

terr = np.zeros((len(keys), 2))
atmo = np.zeros((len(keys), 2))
foss = np.zeros((len(keys), 2))
ocea = np.zeros((len(keys), 2))
gmt = np.zeros((len(keys), 2))
econ = np.zeros((len(keys), 4))

for i, key in enumerate(keys):
    terr[i, 0] = np.mean(results[key]["terr"])
    atmo[i, 0] = np.mean(results[key]["atmo"])
    foss[i, 0] = np.mean(results[key]["foss"])
    ocea[i, 0] = np.mean(results[key]["ocea"])
    econ[i, 0:2] = np.mean(results[key]["econ"], axis=0)
    gmt[i, 0] = np.mean(results[key]["gmt"])

    terr[i, 1] = np.std(results[key]["terr"])
    atmo[i, 1] = np.std(results[key]["atmo"])
    foss[i, 1] = np.std(results[key]["foss"])
    ocea[i, 1] = np.std(results[key]["ocea"])
    gmt[i, 1] = np.std(results[key]["gmt"])
    econ[i, 2:] = np.std(results[key]["econ"], axis=0)

econ[:, 0::2] /= 0.25 * 6e9
econ[:, 1::2] /= 0.75 * 6e9
print(econ)

ax1a = ax2.twinx()
#ax1.scatter(keys, terr[:, 0], alpha=.3, c="g", marker="o", label="Terrestrial carbon")
#ax1.scatter(keys, atmo[:, 0], alpha=.3, c="c", marker="o", label="Atmospheric carbon")
#ax1.scatter(keys, ocea[:, 0], alpha=.3, c="b", marker="o", label="Ocean carbon")
#ax1a.scatter(keys, gmt[:, 0], alpha=.3, c="k", marker="o", label="Global Mean Temperature")

ax1.errorbar(keys, terr[:, 0], yerr=terr[:, 1], fmt='o', c="g", 
             alpha=0.5, label="Terrestrial carbon")
ax1.errorbar(keys, atmo[:, 0], yerr=atmo[:, 1], fmt='o', c="c", 
             alpha=0.5, label="Atmospheric carbon")
ax1.errorbar(keys, ocea[:, 0], yerr=ocea[:, 1], fmt='o', c="b", 
             alpha=0.5, label="Ocean carbon")
ax2.errorbar(keys, econ[:, 0], yerr=econ[:, 2], fmt='o', c="r", 
             alpha=0.5, label="North")
ax2.errorbar(keys, econ[:, 1], yerr=econ[:, 3], fmt='d', c="r", 
             alpha=0.5, label="South")



ax1a.errorbar(keys, gmt[:, 0], yerr=gmt[:, 1], fmt='o', c="k", 
             alpha=0.5, label="Global Mean Temperature")

#ax2.scatter(x, econ[:,0], marker="o", alpha=0.3, label="Social System 1")
#ax2.scatter(x, econ[:,1], marker="o", alpha=0.3, label="Social System 2")
#ax2.plot(x[N-1:], smooth(econ), lw=2)

ax1.legend()
ax1a.legend(loc="upper left")
ax2.legend(loc="center left")

ax1.set_ylabel("Gigatonnes Carbon in 2120")
ax1a.set_ylabel("Global mean temperature in 2120 [K]")
ax2.set_xlabel("Learning rate [$yr^{-1}$]")
ax2.set_ylabel("GDP/capita in 2120 [$/yr]")

data = np.load("core_without_social_u_0.020000000000000004_loweredS0_0.p")
world = list(data["World.surface_air_temperature"].keys())[0]
terr = data["World.terrestrial_carbon"][world][-1]
atmo = data["World.atmospheric_carbon"][world][-1]
foss = data["World.fossil_carbon"][world][-1]
ocea = data["World.upper_ocean_carbon"][world][-1]
gmt = data["World.surface_air_temperature"][world][-1]

ax1.axhline(terr, c="g", ls="--", lw=2) 
ax1.axhline(atmo, c="c", ls="--", lw=2) 
ax1.axhline(ocea, c="b", ls="--", lw=2) 
ax1a.axhline(gmt, c="k", ls="--", lw=2) 

social_systems = list(data["SocialSystem.has_emissions_tax"].keys())
econ = [data["SocialSystem.economic_output_flow"][s][-1] for s in social_systems]
ax2.axhline(econ[0] / 0.25 / 6e9, ls="--", lw=2, c="r")
ax2.axhline(econ[1] / 0.75 / 6e9, ls="--", lw=2, c="r")

ax2.semilogx()
ax2.set_xlim(min(keys), max(keys))
ax1a.set_ylim(287.5, 290)
ax2.semilogy()
plt.tight_layout()
plt.savefig("figure6.pdf")
