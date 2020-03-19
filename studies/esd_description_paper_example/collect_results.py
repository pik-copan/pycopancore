import glob
import numpy as np
import pickle

files=glob.glob("/p/tmp/marcwie/core20190627/*.p")

try:
    results = np.load("results_ensemble.p")
    print("Loading results from disk")
except:
    results = {"succesful_files": []}
    print("Creating new results file")

files = [f for f in files if f not in results["succesful_files"]]
print(len(files))
for i, datafile in enumerate(files):

    print(i, datafile, end="\r")
    updaterate = float(datafile.split("_")[-3])

    if updaterate not in results.keys():
        results[updaterate] = {"terr": [], "atmo": [], "foss": [], "ocea": [],
                               "gmt": [], "econ": []}

    data = np.load(datafile)
    world = list(data["World.surface_air_temperature"].keys())[0]
    terr = data["World.terrestrial_carbon"][world][-1]
    atmo = data["World.atmospheric_carbon"][world][-1]
    foss = data["World.fossil_carbon"][world][-1]
    ocea = data["World.upper_ocean_carbon"][world][-1]
    gmt = data["World.surface_air_temperature"][world][-1]

    social_systems = list(data["SocialSystem.has_emissions_tax"].keys())
    econ = [data["SocialSystem.economic_output_flow"][s][-1] for s in social_systems]
    
    results[updaterate]["terr"].append(terr)
    results[updaterate]["atmo"].append(atmo)
    results[updaterate]["foss"].append(foss)
    results[updaterate]["ocea"].append(ocea)
    results[updaterate]["gmt"].append(gmt)
    results[updaterate]["econ"].append(econ)

    results["succesful_files"].append(datafile)

    pickle.dump(results, open("results_ensemble.p", "wb"))
