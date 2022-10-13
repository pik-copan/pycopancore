import numpy as np
from time import time
import datetime as dt
from numpy import random
import json
import networkx as nx

#---paths and dirs---

# data from which date?
date = "2022_10_12"
# data from which run?

traj_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\mc\\{date}\\traj.pickle"

# will save plots with the SAME date as the data was produced as to prevent confusion
save_dir = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\mc\\{date}"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
    print(f"Directory {date} created @ {save_dir}")

import datetime
current_time = datetime.datetime.now()
current = [current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second]
time_string = f"{current_time.year}"
for i in current:
    if i < 10:
        time_string += f"_0{i}"
    else:
        time_string += f"_{i}"

# text file
with open(save_dir +"\\" +'readme.txt', 'w') as f:
    f.write(f'Data from {date} used.')

save_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{date}\\{run}\\{time_string}"
os.mkdir(save_path)
print(f"Directory {time_string} created @ {save_path}")

#---load data---
configuration = json.load(open(configuration_path))
traj = pickle.load(open(traj_path,"rb"))
t = np.array(traj['t'])
acquaintance_network = pickle.load(open(network_path+"\\"+networks[0]+".pickle","rb"))
group_membership_network = pickle.load(open(network_path+"\\"+networks[1]+".pickle","rb"))
