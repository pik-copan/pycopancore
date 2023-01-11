import numpy as np
import pandas as pd
import json
import pickle
import matplotlib.pyplot as plt


parameter_name_list = ["timeinterval", "timestep", "parameter1", "parameter2", "nindividuals", "nc"]
INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}

# path to data
PATH = f"..\\test"

# load config
CONFIG_LOAD_PATH = PATH + "\\config.json"
config = json.load(open(CONFIG_LOAD_PATH))

parameter_dict = {str(key): value for key, value in config.items() if key in parameter_name_list}

# create key list in dictionary
key_dict = {}
# find max length
max_length = max([len(value) for key, value in parameter_dict.items()])
for n in range(max_length):
    key_list = []
    for key, value in parameter_dict.items():
        if n < len(value):
            key_list.append(value[n])
        else:
            key_list.append(value[0])
    key_dict[f"{n}"] = key_list
# this dictionary can be used to call certain parameter combinations

RAW_LOAD_PATH = PATH + "\\raw\\blablabla.pkl"
raw = pickle.load(open(RAW_LOAD_PATH, "rb"))

RES_LOAD_PATH = PATH + "\\res\\stateval_results.pkl"
data = pd.read_pickle(RES_LOAD_PATH)

data.head()
data['mean'].unstack('observables').xs(key=key_dict["0"], level=parameter_name_list).plot()
data['sem'].unstack('observables').xs(key=key_dict["0"], level=parameter_name_list).plot()
plt.show()